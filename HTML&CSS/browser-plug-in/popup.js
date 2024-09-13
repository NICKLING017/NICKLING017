document.addEventListener('DOMContentLoaded', function() {
  const addCurrentSiteButton = document.getElementById('addCurrentSite');
  const siteList = document.getElementById('siteList');
  const timeStats = document.getElementById('timeStats');
  const fishingStatus = document.createElement('div');
  fishingStatus.id = 'fishingStatus';
  document.body.insertBefore(fishingStatus, timeStats);

  // 加载已保存的网站列表
  loadSites();

  // 添加当前网站
  addCurrentSiteButton.addEventListener('click', function() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      if (tabs[0]) {
        const url = new URL(tabs[0].url);
        const domain = url.hostname;
        addSite(domain);
      }
    });
  });

  // 添加网站
  function addSite(site) {
    chrome.storage.sync.get(['sites'], function(result) {
      const sites = result.sites || [];
      if (!sites.includes(site)) {
        sites.push(site);
        chrome.storage.sync.set({sites: sites}, function() {
          loadSites();
        });
      }
    });
  }

  // 加载网站列表
  function loadSites() {
    chrome.storage.sync.get(['sites'], function(result) {
      const sites = result.sites || [];
      updateSiteList(sites);
    });
  }

  // 更新网站列表显示
  function updateSiteList(sites) {
    siteList.innerHTML = '<h3>监控网站列表：</h3>';
    sites.forEach(function(site) {
      const div = document.createElement('div');
      div.className = 'site-item';
      div.innerHTML = `
        <span>${site}</span>
        <span class="remove-site" data-site="${site}">×</span>
      `;
      siteList.appendChild(div);
    });

    // 添加删除事件监听器
    document.querySelectorAll('.remove-site').forEach(item => {
      item.addEventListener('click', function() {
        removeSite(this.getAttribute('data-site'));
      });
    });
  }

  // 删除网站
  function removeSite(site) {
    chrome.storage.sync.get(['sites'], function(result) {
      let sites = result.sites || [];
      sites = sites.filter(s => s !== site);
      chrome.storage.sync.set({sites: sites}, function() {
        loadSites();
      });
    });
  }

  // 显示时间统计和摸鱼状态
  function updateTimeStats() {
    chrome.runtime.sendMessage({action: "getCurrentStatus"}, function(response) {
      const currentSite = response.currentFishingSite;
      
      // 更新摸鱼状态
      if (currentSite) {
        fishingStatus.textContent = `当前正在摸鱼：${currentSite}`;
        fishingStatus.style.backgroundColor = '#ffcccb';
      } else {
        fishingStatus.textContent = '当前不在摸鱼';
        fishingStatus.style.backgroundColor = '#90EE90';
      }

      chrome.storage.sync.get(['timeStats'], function(result) {
        const stats = result.timeStats || {};
        timeStats.innerHTML = '<h3>浏览时间统计：</h3>';
        for (const site in stats) {
          if (site && site !== 'null') {  // 添加这个检查
            const totalSeconds = Math.round(stats[site]); // 总秒数
            const hours = Math.floor(totalSeconds / 3600);
            const minutes = Math.floor((totalSeconds % 3600) / 60);
            const seconds = totalSeconds % 60;
            
            let timeString = '';
            if (hours > 0) {
              timeString += `${padZero(hours)}小时 `;
            }
            if (hours > 0 || minutes > 0) {
              timeString += `${padZero(minutes)}分钟 `;
            }
            timeString += `${padZero(seconds)}秒`;
            
            const div = document.createElement('div');
            div.className = 'site-item';
            div.textContent = `${site}: ${timeString}`;
            timeStats.appendChild(div);
          }
        }
      });
    });
  }

  // 补零函数
  function padZero(num) {
    return num < 10 ? '0' + num : num;
  }

  // 立即更新时间统计
  updateTimeStats();

  // 每秒更新时间统计
  const intervalId = setInterval(updateTimeStats, 1000);

  // 当弹出窗口关闭时，清除定时器
  window.addEventListener('unload', function() {
    clearInterval(intervalId);
  });

  const resetStatsButton = document.getElementById('resetStats');
  const autoResetCheckbox = document.getElementById('autoReset');

  // 重置统计
  resetStatsButton.addEventListener('click', function() {
    chrome.storage.sync.set({timeStats: {}}, function() {
      updateTimeStats();
    });
  });

  // 加载和保存自动重置设置
  chrome.storage.sync.get(['autoReset'], function(result) {
    autoResetCheckbox.checked = result.autoReset || false;
  });

  autoResetCheckbox.addEventListener('change', function() {
    chrome.storage.sync.set({autoReset: this.checked});
  });

  const customMessageInput = document.getElementById('customMessage');
  const saveCustomMessageButton = document.getElementById('saveCustomMessage');

  // 加载自定义消息
  chrome.storage.sync.get(['customMessage'], function(result) {
    customMessageInput.value = result.customMessage || '您正在摸鱼！';
  });

  // 保存自定义消息
  saveCustomMessageButton.addEventListener('click', function() {
    const message = customMessageInput.value.trim();
    if (message) {
      chrome.storage.sync.set({customMessage: message}, function() {
        alert('自定义消息已保存！');
      });
    }
  });

  const enableNotificationCheckbox = document.getElementById('enableNotification');

  // 加载启用提示设置
  chrome.storage.sync.get(['enableNotification'], function(result) {
    enableNotificationCheckbox.checked = result.enableNotification !== false;
  });

  // 保存启用提示设置
  enableNotificationCheckbox.addEventListener('change', function() {
    chrome.storage.sync.set({enableNotification: this.checked}, function() {
      console.log('启用提示设置已保存:', enableNotificationCheckbox.checked);
    });
  });
});