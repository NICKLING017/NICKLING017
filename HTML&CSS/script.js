function generateHeroCards(team) {
    const containerId = team === 'offense' ? 'offenseHeroCards' : 'defenseHeroCards';
    const inputId = team === 'offense' ? 'offenseHeroCount' : 'defenseHeroCount';
    const container = document.getElementById(containerId);
    const heroCount = document.getElementById(inputId).value;
    
    container.innerHTML = ''; // 清空现有卡片

    for (let i = 0; i < heroCount; i++) {
        const heroCard = document.createElement('div');
        heroCard.className = 'hero-card';
        
        heroCard.innerHTML = `
            <div class="hero-info">
                <img src="hero1.png" class="hero-image" alt="Hero ${i + 1}">
                <p><input type="number" value="10026004" class="ID-input"></p>
                <h3>白石飞鸟</h3>
            </div>
            <div class="separator"></div>
            <div class="hero-settings">
                <div class="attributes-container">
                    <p>等级: <input type="number" value="80" class="attribute-input"></p>
                    <p>星级: <input type="number" value="6" class="attribute-input"></p>
                    <p>阶级: <input type="number" value="25" class="attribute-input"></p>
                </div>
                <div class="attributes-container">
                    <p>(少女元气)技能1: <input type="number" value="25" class="attribute-input"></p>
                    <p>(流行飞弹)技能2: <input type="number" value="25" class="attribute-input"></p>
                    <p>(自我治愈)技能3: <input type="number" value="25" class="attribute-input"></p>
                    <p>(枪破固防)技能4: <input type="number" value="25" class="attribute-input"></p>
                    <p>(气功疗愈)技能5: <input type="number" value="25" class="attribute-input"></p>
                </div>
                <div class="attributes-container">
                    <p>兵种: <select class="troop-type-select">
                        <option value="1级杀手">1级杀手</option>
                        <option value="2级杀手">2级杀手</option>
                        <option value="3级杀手">3级杀手</option>
                        <option value="4级杀手">4级杀手</option>
                        <option value="5级杀手">5级杀手</option>
                    </select></p>
                    <p>部队数量: <input type="number" value="996" class="attribute-input"></p>
                </div>
            </div>
        `;
        
        container.appendChild(heroCard);
    }
}

document.getElementById('offenseHeroCount').addEventListener('input', () => generateHeroCards('offense'));
document.getElementById('defenseHeroCount').addEventListener('input', () => generateHeroCards('defense'));
