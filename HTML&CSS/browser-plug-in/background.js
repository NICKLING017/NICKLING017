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
  const fullPath = urlObj.hostname + urlObj.pathname;
  return monitoredSites.some(site => 
    hostname.includes(site) || fullPath.includes(site)
  );
}

// 更新计时
function updateTimer(tabId, url) {
  if (isMonitoredSite(url)) {
    if (activeTabId !== tabId || currentFishingSite !== new URL(url).hostname) {
      if (activeTabId !== null) {
        stopTimer();
      }
      startTimer(tabId, new URL(url).hostname);
    }
  } else if (activeTabId === tabId) {
    stopTimer();
  }
  // 无论如何，都更新当前状态
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
  if (startTime !== null && activeTabId !== null) {
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