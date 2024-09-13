document.addEventListener('DOMContentLoaded', function() {
  const addSiteButton = document.getElementById('addSite');
  const siteInput = document.getElementById('siteInput');
  const siteList = document.getElementById('siteList');
  const timeStats = document.getElementById('timeStats');
  const fishingStatus = document.createElement('div');
  fishingStatus.id = 'fishingStatus';
  document.body.insertBefore(fishingStatus, timeStats);

  // 加载已保存的网站列表
  loadSites();

  // 添加网站
  addSiteButton.addEventListener('click', function() {
    const site = siteInput.value.trim();
    if (site) {
      chrome.storage.sync.get(['sites'], function(result) {
        const sites = result.sites || [];
        if (!sites.includes(site)) {
          sites.push(site);
          chrome.storage.sync.set({sites: sites}, function() {
            loadSites();
            siteInput.value = '';
          });
        }
      });
    }
  });

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
        fishingStatus.style.color = 'red';
      } else {
        fishingStatus.textContent = '当前不在摸鱼';
        fishingStatus.style.color = 'green';
      }

      chrome.storage.sync.get(['timeStats'], function(result) {
        const stats = result.timeStats || {};
        timeStats.innerHTML = '<h3>浏览时间统计：</h3>';
        for (const site in stats) {
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
          div.textContent = `${site}: ${timeString}`;
          timeStats.appendChild(div);
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
});