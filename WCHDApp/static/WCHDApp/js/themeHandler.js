function initTheme() {
    const body = document.body;
    const toggleThemeCheckbox = document.getElementById('toggleTheme');
    const themeSelector = document.getElementById('themeSelector');
    const container = document.getElementById('dragBoxContainer');
    let currentTheme = localStorage.getItem('selectedTheme') || 'default';
    const isDarkMode = localStorage.getItem('theme') === 'dark';
    const colorPalette = document.getElementById('colorPalette');
    const initialOrder = Array.from(container ? container.children : []).map(box => box.dataset.id);

    function setDefaultBoxColor(theme) {
        switch (theme) {
            case 'blue': return '#1976d2';
            case 'green': return '#388e3c';
            case 'pink': return '#c2185b';
            case 'purple': return '#512da8';
            default: return '#3498db';
        }
    }

    function applyBoxStyle(box, backgroundColor, textColor) {
        if (box) {
            const savedColors = JSON.parse(localStorage.getItem('boxColors') || '{}');
            if (backgroundColor !== undefined) {
                box.style.backgroundColor = backgroundColor;
                box.style.color = textColor !== undefined ? textColor : (body.classList.contains('dark-mode') ? 'white' : '');
                savedColors[box.dataset.id] = backgroundColor;
                localStorage.setItem('boxColors', JSON.stringify(savedColors));
            } else if (savedColors[box.dataset.id]) {
                box.style.backgroundColor = savedColors[box.dataset.id];
                box.style.color = getContrastColor(savedColors[box.dataset.id]);
            } else {
                const themeColor = currentTheme === 'default' ? '#3498db' : setDefaultBoxColor(currentTheme);
                box.style.backgroundColor = themeColor;
                box.style.color = body.classList.contains('dark-mode') ? 'white' : '';
            }
        }
    }

    function getContrastColor(hexcolor) {
        hexcolor = hexcolor.replace("#", "");
        const r = parseInt(hexcolor.substr(0, 2), 16);
        const g = parseInt(hexcolor.substr(2, 2), 16);
        const b = parseInt(hexcolor.substr(4, 2), 16);
        const yiq = ((r * 299) + (g * 587) + (b * 114)) / 1000;
        return (yiq >= 128) ? 'black' : 'white';
    }

    function applyThemeToAllBoxes(theme, isDark) {
        if (container) {
            const themeColor = theme === 'default' ? '#3498db' : setDefaultBoxColor(theme);
            const textColor = isDark ? 'white' : '';
            [...container.children].forEach(box => {
                const savedColors = JSON.parse(localStorage.getItem('boxColors') || '{}');
                if (!savedColors[box.dataset.id]) {
                    applyBoxStyle(box, themeColor, textColor);
                }
            });
        }
    }

    function resetLayout() {
        if (container) {
            localStorage.removeItem('boxColors');
            const boxes = Array.from(container.children);
            boxes.sort((a, b) => {
                const indexA = initialOrder.indexOf(a.dataset.id);
                const indexB = initialOrder.indexOf(b.dataset.id);
                return indexA - indexB;
            });
            boxes.forEach(box => container.appendChild(box));
            const currentThemeForReset = localStorage.getItem('selectedTheme') || 'default';
            const isDarkModeForReset = localStorage.getItem('theme') === 'dark';
            applyThemeToAllBoxes(currentThemeForReset, isDarkModeForReset);
        }
    }

    function initColorPalette() {
        const colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#d35400', '#c0392b'];
        colors.forEach(color => {
            const colorBox = document.createElement('div');
            colorBox.classList.add('color-option');
            colorBox.style.backgroundColor = color;
            colorBox.addEventListener('click', function() {
                if (colorPalette.activeBox) {
                    applyBoxStyle(colorPalette.activeBox, color, getContrastColor(color));
                    colorPalette.style.display = 'none';
                    colorPalette.activeBox = null;
                }
            });
            colorPalette.appendChild(colorBox);
        });
        document.addEventListener('click', function(event) {
            if (!colorPalette.contains(event.target) && event.target !== colorPalette.activeBox) {
                colorPalette.style.display = 'none';
                colorPalette.activeBox = null;
            }
        });
    }

    if (isDarkMode) {
        body.classList.add('dark-mode');
        if (toggleThemeCheckbox) {
            toggleThemeCheckbox.checked = true;
        }
    }

    const savedTheme = localStorage.getItem('selectedTheme');
    body.classList.remove('blue-theme', 'green-theme', 'pink-theme', 'purple-theme');
    if (savedTheme && savedTheme !== 'default') {
        body.classList.add(`${savedTheme}-theme`);
        if (themeSelector) {
            themeSelector.value = savedTheme;
            currentTheme = savedTheme;
            applyThemeToAllBoxes(savedTheme, isDarkMode);
        }
    } else if (themeSelector) {
        themeSelector.value = 'default';
        currentTheme = 'default';
        applyThemeToAllBoxes('default', isDarkMode);
    }

    if (toggleThemeCheckbox) {
        toggleThemeCheckbox.addEventListener('change', () => {
            const dark = !body.classList.contains('dark-mode');
            body.classList.toggle('dark-mode');
            localStorage.setItem('theme', dark ? 'dark' : 'light');
            const currentThemeOnToggle = localStorage.getItem('selectedTheme') || 'default';
            applyThemeToAllBoxes(currentThemeOnToggle, dark);
        });
    }

    if (themeSelector) {
        themeSelector.addEventListener('change', function() {
            const selectedTheme = this.value;
            body.classList.remove('blue-theme', 'green-theme', 'pink-theme', 'purple-theme');
            if (selectedTheme !== 'default') {
                body.classList.add(`${selectedTheme}-theme`);
                localStorage.setItem('selectedTheme', selectedTheme);
                currentTheme = selectedTheme;
                applyThemeToAllBoxes(selectedTheme, body.classList.contains('dark-mode'));
            } else {
                localStorage.removeItem('selectedTheme');
                currentTheme = 'default';
                applyThemeToAllBoxes('default', body.classList.contains('dark-mode'));
            }
        });
    }

    if (container) {
        container.addEventListener('contextmenu', function(event) {
            event.preventDefault();
            const targetBox = event.target.closest('.box');
            if (targetBox) {
                colorPalette.style.display = 'block';
                colorPalette.style.position = 'fixed';
                colorPalette.style.left = event.clientX + 'px';
                colorPalette.style.top = event.clientY + 'px';
                colorPalette.activeBox = targetBox;
            }
        });
    }

    const resetButton = document.getElementById('resetOrderBtn');
    if (resetButton) {
        resetButton.addEventListener('click', resetLayout);
    }

    initColorPalette();
    applyThemeToAllBoxes(currentTheme, isDarkMode);
}