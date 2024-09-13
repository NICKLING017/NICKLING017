let activeTabId = null;
let startTime = null;
let monitoredSites = [];
let currentFishingSite = null;

// 加载监控网站列表
function loadMonitoredSites() {
  chrome.storage.sync.get(['sites'], function(result) {
    monitoredSites = result.sites || [];
  });
}

// 初始加载
loadMonitoredSites();

// 监听存储变化，更新监控网站列表
chrome.storage.onChanged.addListener(function(changes, namespace) {
  if (namespace === 'sync' && changes.sites) {
    monitoredSites = changes.sites.newValue;
  }
});

// 检查URL是否在监控列表中
function isMonitoredSite(url) {
  const urlObj = new URL(url);
  const hostname = urlObj.hostname;
  return monitoredSites.some(site => hostname.includes(site));
}

// 更新计时
function updateTimer(tabId, url) {
  const isFishing = isMonitoredSite(url);
  if (isFishing) {
    if (activeTabId !== tabId || currentFishingSite !== new URL(url).hostname) {
      if (activeTabId !== null) {
        stopTimer();
      }
      startTimer(tabId, new URL(url).hostname);
      
      chrome.storage.sync.get(['enableNotification', 'customMessage'], function(result) {
        console.log('启用提示设置:', result.enableNotification); // 添加这行日志
        if (result.enableNotification !== false) { // 默认为true
          // 注入 CSS
          chrome.tabs.insertCSS(tabId, {file: "content.css"}, function() {
            if (chrome.runtime.lastError) {
              console.log('Error inserting CSS:', chrome.runtime.lastError);
            }
          });

          // 注入并执行脚本
          chrome.tabs.executeScript(tabId, {file: "content.js"}, function() {
            if (chrome.runtime.lastError) {
              console.log('Error executing script:', chrome.runtime.lastError);
            } else {
              const message = result.customMessage || '您正在摸鱼！';
              chrome.tabs.sendMessage(tabId, {
                action: 'showNotification',
                message: message
              }, function(response) {
                if (chrome.runtime.lastError) {
                  console.log('Error sending message:', chrome.runtime.lastError);
                } else {
                  console.log('Message sent successfully');
                }
              });
            }
          });
        }
      });
    }
  } else if (activeTabId === tabId) {
    stopTimer();
  }
  updateCurrentStatus();
}

// 开始计时
function startTimer(tabId, hostname) {
  activeTabId = tabId;
  startTime = Date.now();
  currentFishingSite = hostname;
  updateCurrentStatus();
}

// 停止计时
function stopTimer() {
  if (startTime !== null && activeTabId !== null && currentFishingSite) {
    const duration = (Date.now() - startTime) / 1000; // 转换为秒
    
    console.log(`停止计时: ${currentFishingSite}, 持续时间: ${duration}秒`);
    
    chrome.storage.sync.get(['timeStats'], function(result) {
      let stats = result.timeStats || {};
      stats[currentFishingSite] = (stats[currentFishingSite] || 0) + duration;
      chrome.storage.sync.set({timeStats: stats});
    });

    activeTabId = null;
    startTime = null;
    currentFishingSite = null;
    updateCurrentStatus();
    updateBadge(false); // 添加这行
  }
}

// 更新当前状态
function updateCurrentStatus() {
  if (currentFishingSite) {
    chrome.storage.sync.set({currentFishingSite: currentFishingSite});
  } else {
    chrome.storage.sync.remove('currentFishingSite');
  }
}

// 监听标签更新
chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
  if (changeInfo.url) {
    updateTimer(tabId, changeInfo.url);
  }
});

// 监听标签激活
chrome.tabs.onActivated.addListener(function(activeInfo) {
  chrome.tabs.get(activeInfo.tabId, function(tab) {
    updateTimer(tab.id, tab.url);
  });
});

// 监听窗口焦点变化
chrome.windows.onFocusChanged.addListener(function(windowId) {
  if (windowId === chrome.windows.WINDOW_ID_NONE) {
    stopTimer();
  } else {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      if (tabs.length > 0) {
        updateTimer(tabs[0].id, tabs[0].url);
      }
    });
  }
});

// 检查并执行每日重置
function checkAndResetDaily() {
  chrome.storage.sync.get(['lastResetDate', 'autoReset'], function(result) {
    const today = new Date().toDateString();
    if (result.autoReset && result.lastResetDate !== today) {
      chrome.storage.sync.set({timeStats: {}, lastResetDate: today});
    }
  });
}

// 每小时检查一次是否需要重置
setInterval(checkAndResetDaily, 3600000); // 3600000 毫秒 = 1 小时

// 在浏览器启动时也检查一次
chrome.runtime.onStartup.addListener(checkAndResetDaily);

// 监听来自popup的消息
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === "getCurrentStatus") {
    // 确保在发送响应之前获取最新状态
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      if (tabs.length > 0) {
        updateTimer(tabs[0].id, tabs[0].url);
      }
      sendResponse({currentFishingSite: currentFishingSite});
    });
    return true; // 表示我们会异步发送响应
  } else if (request.action === "resetStats") {
    chrome.storage.sync.set({timeStats: {}}, function() {
      sendResponse({success: true});
    });
    return true; // 表示我们会异步发送响应
  }
});

// 定期更新存储中的时间（每1秒更新一次）
setInterval(function() {
  if (startTime !== null && activeTabId !== null && currentFishingSite) {
    const duration = (Date.now() - startTime) / 1000; // 转换为秒
    chrome.storage.sync.get(['timeStats'], function(result) {
      let stats = result.timeStats || {};
      stats[currentFishingSite] = (stats[currentFishingSite] || 0) + duration;
      chrome.storage.sync.set({timeStats: stats});
    });
    startTime = Date.now(); // 重置开始时间
    updateCurrentStatus(); // 确保当前状态始终是最新的
  }
}, 1000); // 每1秒更新一次

// 添加这个新函数
function updateBadge(isFishing) {
  if (isFishing) {
    chrome.browserAction.setBadgeText({text: '摸鱼'});
    chrome.browserAction.setBadgeBackgroundColor({color: '#FF0000'}); // 红色背景
  } else {
    chrome.browserAction.setBadgeText({text: ''});
  }
}

// 在浏览器启动时初始化 badge
chrome.runtime.onStartup.addListener(function() {
  updateBadge(false);
});

// 在插件安装或更新时初始化 badge
chrome.runtime.onInstalled.addListener(function() {
  updateBadge(false);
});