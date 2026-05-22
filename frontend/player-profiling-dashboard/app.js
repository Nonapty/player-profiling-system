const API_BASE = "/api/v1";

const els = {
  playerCombo: document.getElementById("playerCombo"),
  compareCombo: document.getElementById("compareCombo"),
  playerSearch: document.getElementById("playerSearch"),
  compareSearch: document.getElementById("compareSearch"),
  playerOptions: document.getElementById("playerOptions"),
  compareOptions: document.getElementById("compareOptions"),
  playerName: document.getElementById("playerName"),
  playerMeta: document.getElementById("playerMeta"),
  scoreValue: document.getElementById("scoreValue"),
  pointsMetric: document.getElementById("pointsMetric"),
  assistsMetric: document.getElementById("assistsMetric"),
  reboundsMetric: document.getElementById("reboundsMetric"),
  styleMetric: document.getElementById("styleMetric"),
  pointsBar: document.getElementById("pointsBar"),
  assistsBar: document.getElementById("assistsBar"),
  reboundsBar: document.getElementById("reboundsBar"),
  clusterMetric: document.getElementById("clusterMetric"),
  scoreGauge: document.getElementById("scoreGauge"),
  radarChart: document.getElementById("radarChart"),
  trendChart: document.getElementById("trendChart"),
  spaceChart: document.getElementById("spaceChart"),
  similarList: document.getElementById("similarList"),
  explainChart: document.getElementById("explainChart"),
  compareChart: document.getElementById("compareChart"),
  compareTitle: document.getElementById("compareTitle")
};

let players = [];
let currentDashboard = null;
let currentCompare = null;
let currentCompareDashboard = null;
let selectedPlayerId = "";
let selectedCompareId = "";

const labelMap = {
  Scoring: "得分",
  Playmaking: "组织",
  Rebounding: "篮板",
  Efficiency: "效率",
  Defense: "防守",
  Shooting: "投射",
  points: "得分",
  assists: "助攻",
  rebounds: "篮板"
};

const styleMap = {
  "All-around creator": "全能组织核心",
  "Perimeter scorer": "外线得分手",
  "Playmaking big": "策应型内线",
  "Rim pressure": "篮下冲击型",
  "High-usage creator": "高持球核心",
  "Two-way wing": "攻防锋线",
  Balanced: "均衡型"
};

const positionMap = {
  Forward: "前锋",
  Guard: "后卫",
  Center: "中锋",
  PG: "控卫",
  SG: "分卫",
  SF: "小前锋",
  PF: "大前锋",
  C: "中锋",
  Player: "球员"
};

const positionAliasMap = {
  PG: ["控卫", "组织后卫", "后卫"],
  SG: ["分卫", "得分后卫", "后卫"],
  SF: ["小前锋", "锋线", "前锋"],
  PF: ["大前锋", "锋线", "前锋", "内线"],
  C: ["中锋", "内线"],
  Guard: ["后卫"],
  Forward: ["前锋", "锋线"],
  Center: ["中锋", "内线"]
};

async function getJson(path) {
  const response = await fetch(path);
  if (!response.ok) {
    throw new Error(`Request failed: ${path}`);
  }
  const payload = await response.json();
  return payload.data;
}

function playerLabel(player) {
  return player.name || player.player_id;
}

function zhStyle(style) {
  return styleMap[style] || style || "均衡型";
}

function zhPosition(position) {
  return positionMap[position] || position || "球员";
}

function zhLabel(label) {
  return labelMap[label] || label;
}

function firstOtherPlayerId(playerId) {
  return players.find((player) => player.player_id !== playerId)?.player_id || playerId;
}

function playerById(playerId) {
  return players.find((player) => player.player_id === playerId);
}

function searchableText(player) {
  const positionAliases = positionAliasMap[player.position] || [];
  return [
    player.name,
    player.team,
    player.position,
    zhPosition(player.position),
    ...positionAliases,
    player.player_id
  ].join(" ").toLowerCase();
}

function syncCompareSelection() {
  if (!selectedCompareId || selectedCompareId === selectedPlayerId || !playerById(selectedCompareId)) {
    selectedCompareId = firstOtherPlayerId(selectedPlayerId);
  }
}

function setComboValues() {
  const player = playerById(selectedPlayerId);
  const compare = playerById(selectedCompareId);
  els.playerSearch.value = player ? playerLabel(player) : "";
  els.compareSearch.value = compare ? playerLabel(compare) : "";
}

function filteredPlayers(kind, query) {
  const normalized = query.trim().toLowerCase();
  return players
    .filter((player) => kind !== "compare" || player.player_id !== selectedPlayerId)
    .filter((player) => !normalized || searchableText(player).includes(normalized))
    .slice(0, 12);
}

function renderComboOptions(kind, query = "") {
  const optionsEl = kind === "player" ? els.playerOptions : els.compareOptions;
  const selectedId = kind === "player" ? selectedPlayerId : selectedCompareId;
  const matches = filteredPlayers(kind, query);

  if (!matches.length) {
    optionsEl.innerHTML = `<div class="combo-empty">无匹配球员</div>`;
    return;
  }

  optionsEl.innerHTML = matches.map((player) => `
    <button class="combo-option ${player.player_id === selectedId ? "selected" : ""}" type="button" data-player-id="${player.player_id}">
      <strong>${playerLabel(player)}</strong>
      <span>${player.team || "未知球队"} · ${zhPosition(player.position)}</span>
    </button>
  `).join("");
}

function openCombo(kind) {
  const combo = kind === "player" ? els.playerCombo : els.compareCombo;
  const input = kind === "player" ? els.playerSearch : els.compareSearch;
  combo.classList.add("open");
  renderComboOptions(kind, input.value);
}

function closeCombos() {
  els.playerCombo.classList.remove("open");
  els.compareCombo.classList.remove("open");
}

function selectComboPlayer(kind, playerId) {
  if (kind === "player") {
    selectedPlayerId = playerId;
    syncCompareSelection();
  } else {
    selectedCompareId = playerId;
  }
  setComboValues();
  closeCombos();
  renderDashboard();
}

function initCombo(kind) {
  const input = kind === "player" ? els.playerSearch : els.compareSearch;
  const optionsEl = kind === "player" ? els.playerOptions : els.compareOptions;

  input.addEventListener("focus", () => openCombo(kind));
  input.addEventListener("input", () => openCombo(kind));
  input.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      const firstOption = optionsEl.querySelector(".combo-option");
      if (firstOption) {
        event.preventDefault();
        selectComboPlayer(kind, firstOption.dataset.playerId);
      }
    }
    if (event.key === "Escape") {
      closeCombos();
      setComboValues();
    }
  });

  optionsEl.addEventListener("click", (event) => {
    const option = event.target.closest(".combo-option");
    if (option) {
      selectComboPlayer(kind, option.dataset.playerId);
    }
  });
}

function scoreFromFeatures(features) {
  const value = features.vector.reduce((sum, item) => sum + item, 0) / features.vector.length;
  return Math.round(value * 100);
}

function featureLevel(value) {
  if (value >= 0.7) return "优势";
  if (value >= 0.45) return "稳定";
  return "短板";
}

function isFocused(panelId) {
  return document.getElementById(panelId)?.classList.contains("focused");
}

function renderVisuals(dashboard, compare, compareDashboard) {
  renderRadar(dashboard.features, dashboard.player.stats, dashboard.player, compareDashboard);
  renderTrend(dashboard.trend, compareDashboard?.trend, dashboard.player, compareDashboard?.player);
  renderSpace(dashboard.style_space, dashboard.player.player_id);
  renderSimilar(dashboard.similarity, dashboard.player);
  renderExplanation(dashboard.explanation);
  renderCompare(compare);
}

function renderOverview(data) {
  const { player, features } = data;
  const stats = player.stats;

  els.playerName.textContent = playerLabel(player);
  els.playerMeta.textContent = `${player.team || "未知球队"} · ${zhPosition(player.position)} · ${player.season} · ${zhStyle(player.style)}`;
  els.pointsMetric.textContent = stats.points.toFixed(1);
  els.assistsMetric.textContent = stats.assists.toFixed(1);
  els.reboundsMetric.textContent = stats.rebounds.toFixed(1);
  els.styleMetric.textContent = zhStyle(player.style);
  els.clusterMetric.textContent = `聚类 ${data.cluster.cluster_id}`;
  els.pointsBar.style.width = `${Math.min(stats.points / 35 * 100, 100)}%`;
  els.assistsBar.style.width = `${Math.min(stats.assists / 11 * 100, 100)}%`;
  els.reboundsBar.style.width = `${Math.min(stats.rebounds / 13 * 100, 100)}%`;

  const score = scoreFromFeatures(features);
  els.scoreValue.textContent = score;
  els.scoreGauge.style.setProperty("--score", `${score}%`);
}

function renderRadar(features, stats, player, compareDashboard) {
  const focused = isFocused("profile");
  const labels = features.labels;
  const values = features.vector;
  const compareValues = compareDashboard?.features?.vector || [];
  const compareName = compareDashboard?.player ? playerLabel(compareDashboard.player) : "";
  const size = focused ? 310 : 280;
  const center = size / 2;
  const radius = focused ? 96 : 88;
  const levels = [0.25, 0.5, 0.75, 1];

  const pointsFor = (scale, sourceValues = values) => labels.map((_, index) => {
    const angle = -Math.PI / 2 + index * (Math.PI * 2 / labels.length);
    const value = (sourceValues[index] || 0) * scale;
    return `${center + Math.cos(angle) * radius * value},${center + Math.sin(angle) * radius * value}`;
  }).join(" ");

  const grid = levels.map((level) => `<polygon points="${pointsFor(level)}" fill="none" stroke="#ded8cf" stroke-width="1" />`).join("");
  const axes = labels.map((label, index) => {
    const angle = -Math.PI / 2 + index * (Math.PI * 2 / labels.length);
    const x = center + Math.cos(angle) * (radius + 32);
    const y = center + Math.sin(angle) * (radius + 32);
    const lineX = center + Math.cos(angle) * radius;
    const lineY = center + Math.sin(angle) * radius;
    return `
      <line x1="${center}" y1="${center}" x2="${lineX}" y2="${lineY}" stroke="#ded8cf" />
      <text class="axis-label" x="${x}" y="${y}" text-anchor="middle" dominant-baseline="middle">${zhLabel(label)}</text>
    `;
  }).join("");

  els.radarChart.innerHTML = `
    <svg viewBox="0 0 ${size} ${size}" role="img" aria-label="Ability radar chart">
      ${grid}
      ${axes}
      ${compareValues.length ? `<polygon points="${pointsFor(1, compareValues)}" fill="rgba(215, 154, 43, 0.18)" stroke="#d79a2b" stroke-width="2.4" stroke-dasharray="6 5" />` : ""}
      <polygon points="${pointsFor(1)}" fill="rgba(25, 123, 122, 0.26)" stroke="#197b7a" stroke-width="3" />
      ${compareValues.length ? `
        <g class="chart-legend">
          <circle cx="${size - 88}" cy="18" r="4" fill="#197b7a" />
          <text x="${size - 78}" y="22">${playerLabel(player)}</text>
          <circle cx="${size - 88}" cy="36" r="4" fill="#d79a2b" />
          <text x="${size - 78}" y="40">${compareName}</text>
        </g>
      ` : ""}
      ${focused ? `
        <rect x="12" y="${size - 58}" width="138" height="42" rx="8" fill="#fbfaf7" stroke="#d7d0c6" />
        <text class="chart-note-title" x="24" y="${size - 38}" text-anchor="start">场均基础数据</text>
        <text class="chart-note" x="24" y="${size - 20}" text-anchor="start">${stats.points.toFixed(1)}分 · ${stats.assists.toFixed(1)}助 · ${stats.rebounds.toFixed(1)}板</text>
      ` : ""}
      ${values.map((value, index) => {
        const angle = -Math.PI / 2 + index * (Math.PI * 2 / labels.length);
        const x = center + Math.cos(angle) * radius * value;
        const y = center + Math.sin(angle) * radius * value;
        const labelX = center + Math.cos(angle) * (radius * value + 28);
        const labelY = center + Math.sin(angle) * (radius * value + 28);
        return `
          <circle cx="${x}" cy="${y}" r="${focused ? 6 : 5}" fill="#d85c47" />
          ${focused ? `
            <text class="radar-value-label" x="${labelX}" y="${labelY - 5}" text-anchor="middle">${Math.round(value * 100)}</text>
            <text class="radar-level-label" x="${labelX}" y="${labelY + 10}" text-anchor="middle">${featureLevel(value)}</text>
          ` : ""}
        `;
      }).join("")}
    </svg>
  `;
}

function renderTrend(trend, compareTrend, player, comparePlayer) {
  const focused = isFocused("trendPanel");
  const width = focused ? 580 : 520;
  const height = focused ? 340 : 330;
  const pad = 36;
  const barBase = height - 34;
  const values = trend.values;
  const compareValues = compareTrend?.values || [];
  const allValues = [...values, ...compareValues];
  const min = Math.min(...allValues) - 1;
  const max = Math.max(...allValues) + 1;
  const avg = values.reduce((sum, value) => sum + value, 0) / values.length;
  const peak = Math.max(...values);
  const peakIndex = values.indexOf(peak);
  const scaleX = (index) => pad + index * ((width - pad * 2) / (values.length - 1));
  const scaleY = (value) => height - 78 - ((value - min) / (max - min)) * (height - 110);
  const peakLabelY = Math.max(34, scaleY(peak) - 24);
  const path = values.map((value, index) => `${index === 0 ? "M" : "L"} ${scaleX(index)} ${scaleY(value)}`).join(" ");
  const comparePath = compareValues.map((value, index) => `${index === 0 ? "M" : "L"} ${scaleX(index)} ${scaleY(value)}`).join(" ");
  const area = `${path} L ${scaleX(values.length - 1)} ${barBase - 36} L ${scaleX(0)} ${barBase - 36} Z`;

  els.trendChart.innerHTML = `
    <svg class="trend-svg" viewBox="0 0 ${width} ${height}" role="img" aria-label="近期状态趋势图">
      <defs>
        <linearGradient id="trendFill" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#d85c47" stop-opacity="0.32" />
          <stop offset="100%" stop-color="#d85c47" stop-opacity="0.04" />
        </linearGradient>
      </defs>
      <rect x="10" y="8" width="${width - 20}" height="${height - 16}" rx="8" fill="#fbfaf7" />
      ${[0.25, 0.5, 0.75].map((ratio) => {
        const y = 24 + ratio * (height - 118);
        return `<line x1="${pad}" y1="${y}" x2="${width - pad}" y2="${y}" stroke="#e4ded5" stroke-dasharray="5 8" />`;
      }).join("")}
      <path d="${area}" fill="url(#trendFill)" />
      ${compareValues.length ? `<path d="${comparePath}" fill="none" stroke="#d79a2b" stroke-width="3" stroke-dasharray="7 6" stroke-linecap="round" stroke-linejoin="round" />` : ""}
      <path d="${path}" fill="none" stroke="#d85c47" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" />
      <line x1="${pad}" y1="${scaleY(avg)}" x2="${width - pad}" y2="${scaleY(avg)}" stroke="#197b7a" stroke-width="2" stroke-dasharray="7 7" />
      <text class="tick-label" x="${width - pad}" y="${scaleY(avg) - 8}" text-anchor="end">均值 ${avg.toFixed(1)}</text>
      ${compareValues.map((value, index) => `
        <circle cx="${scaleX(index)}" cy="${scaleY(value)}" r="4" fill="#fbfaf7" stroke="#d79a2b" stroke-width="2.5" />
      `).join("")}
      ${values.map((value, index) => `
        <circle cx="${scaleX(index)}" cy="${scaleY(value)}" r="5" fill="#ffffff" stroke="#d85c47" stroke-width="3" />
        <rect x="${scaleX(index) - 10}" y="${barBase - (value - min) * 8}" width="20" height="${(value - min) * 8}" rx="5" fill="rgba(25, 123, 122, 0.22)" />
        ${focused && index !== peakIndex ? `<text class="point-value-label" x="${scaleX(index)}" y="${scaleY(value) - 14}" text-anchor="middle">${value.toFixed(1)}</text>` : ""}
        <text class="tick-label" x="${scaleX(index)}" y="${height - 12}" text-anchor="middle">${trend.labels[index]}</text>
      `).join("")}
      <circle cx="${scaleX(peakIndex)}" cy="${scaleY(peak)}" r="10" fill="none" stroke="#d79a2b" stroke-width="3" />
      <text class="trend-peak" x="${scaleX(peakIndex)}" y="${peakLabelY}" text-anchor="middle">峰值 ${peak.toFixed(1)}</text>
      <text class="tick-label" x="${pad}" y="25">高 ${max.toFixed(1)}</text>
      <text class="tick-label" x="${pad}" y="${barBase + 10}">低 ${min.toFixed(1)}</text>
      ${compareValues.length ? `
        <g class="chart-legend">
          <circle cx="${width - 142}" cy="${height - 56}" r="4" fill="#d85c47" />
          <text x="${width - 132}" y="${height - 52}">${playerLabel(player)}</text>
          <circle cx="${width - 142}" cy="${height - 37}" r="4" fill="#d79a2b" />
          <text x="${width - 132}" y="${height - 33}">${playerLabel(comparePlayer)}</text>
        </g>
      ` : ""}
    </svg>
  `;
}

function renderSpace(styleSpace, activeId) {
  const focused = isFocused("space");
  const width = focused ? 760 : 700;
  const height = focused ? 400 : 390;
  const pad = 54;
  const colors = ["#647074", "#d85c47", "#197b7a", "#d79a2b", "#3f8b5b"];
  const plotWidth = width - pad * 2;
  const plotHeight = height - pad * 2;
  const placed = [];
  const denseMode = styleSpace.points.length > 40;
  const activePoint = styleSpace.points.find((point) => point.player_id === activeId);
  const sameClusterCount = styleSpace.points.filter((point) => point.cluster_id === activePoint?.cluster_id).length;

  const resolvePoint = (point, index) => {
    let x = pad + point.x * plotWidth;
    let y = height - pad - point.y * plotHeight;
    const minGap = 28;
    let guard = 0;

    while (placed.some((other) => Math.hypot(other.x - x, other.y - y) < minGap) && guard < 18) {
      const angle = index * 1.9 + guard * 0.95;
      const step = 9 + guard * 2.6;
      x += Math.cos(angle) * step;
      y += Math.sin(angle) * step;
      x = Math.max(pad + 14, Math.min(width - pad - 14, x));
      y = Math.max(pad + 14, Math.min(height - pad - 14, y));
      guard += 1;
    }

    placed.push({ x, y });
    return { x, y };
  };

  els.spaceChart.innerHTML = `
    <svg viewBox="0 0 ${width} ${height}" role="img" aria-label="风格空间图">
      <rect x="${pad}" y="${pad}" width="${plotWidth / 2}" height="${plotHeight / 2}" fill="rgba(25, 123, 122, 0.08)" />
      <rect x="${pad + plotWidth / 2}" y="${pad}" width="${plotWidth / 2}" height="${plotHeight / 2}" fill="rgba(63, 139, 91, 0.09)" />
      <rect x="${pad}" y="${pad + plotHeight / 2}" width="${plotWidth / 2}" height="${plotHeight / 2}" fill="rgba(215, 154, 43, 0.1)" />
      <rect x="${pad + plotWidth / 2}" y="${pad + plotHeight / 2}" width="${plotWidth / 2}" height="${plotHeight / 2}" fill="rgba(216, 92, 71, 0.09)" />
      <rect x="${pad}" y="${pad}" width="${plotWidth}" height="${plotHeight}" fill="none" stroke="#d7d0c6" rx="8" />
      <line x1="${width / 2}" y1="${pad}" x2="${width / 2}" y2="${height - pad}" stroke="#d7d0c6" stroke-dasharray="6 7" />
      <line x1="${pad}" y1="${height / 2}" x2="${width - pad}" y2="${height / 2}" stroke="#d7d0c6" stroke-dasharray="6 7" />
      <text class="quadrant-label" x="${pad + 16}" y="${pad + 24}">内线支点</text>
      <text class="quadrant-label" x="${width - pad - 16}" y="${pad + 24}" text-anchor="end">全能核心</text>
      <text class="quadrant-label" x="${pad + 16}" y="${height - pad - 14}">角色拼图</text>
      <text class="quadrant-label" x="${width - pad - 16}" y="${height - pad - 14}" text-anchor="end">外线火力</text>
      <text class="axis-label" x="${width / 2}" y="${height - 12}" text-anchor="middle">进攻创造 →</text>
      <text class="axis-label" x="18" y="${height / 2}" transform="rotate(-90 18 ${height / 2})" text-anchor="middle">内线影响 →</text>
      ${styleSpace.points.map((point, index) => {
        const { x, y } = resolvePoint(point, index);
        const active = point.player_id === activeId;
        const initials = point.name.split(" ").map((part) => part[0]).join("").slice(0, 2);
        const radius = denseMode && !active ? 5 : (active ? 16 : 12);
        return `
          <g class="space-node" data-player-id="${point.player_id}">
          ${active ? `<circle cx="${x}" cy="${y}" r="26" fill="none" stroke="#1f2a2e" stroke-width="2.5" stroke-dasharray="5 5" />` : ""}
          <circle cx="${x}" cy="${y}" r="${radius}" fill="${colors[point.cluster_id % colors.length]}" opacity="${active ? "1" : "0.58"}" stroke="#fff" stroke-width="${denseMode && !active ? 1.5 : 3}" />
          ${denseMode && !active ? "" : `<text class="node-initial" x="${x}" y="${y + 4}" text-anchor="middle">${initials}</text>`}
          ${active ? `
            ${focused ? `
              <rect class="space-callout-box" x="${Math.min(x + 22, width - pad - 178)}" y="${Math.max(y - 10, pad + 8)}" width="176" height="58" rx="8" />
            ` : ""}
            <text class="point-label active-label" x="${x + 24}" y="${y - 20}">${point.name}</text>
            ${focused ? `
              <text class="space-callout-title" x="${Math.min(x + 36, width - pad - 164)}" y="${Math.max(y + 10, pad + 28)}">聚类 ${point.cluster_id} · ${sameClusterCount}人</text>
              <text class="space-callout" x="${Math.min(x + 36, width - pad - 164)}" y="${Math.max(y + 31, pad + 49)}">创造 ${point.x.toFixed(2)} / 内线 ${point.y.toFixed(2)}</text>
            ` : ""}
          ` : ""}
          </g>
        `;
      }).join("")}
    </svg>
  `;

  els.spaceChart.querySelectorAll(".space-node").forEach((node) => {
    node.addEventListener("click", (event) => {
      event.stopPropagation();
      selectedPlayerId = node.dataset.playerId;
      syncCompareSelection();
      setComboValues();
      renderDashboard();
    });
  });
}

function renderSimilar(similarity, player) {
  const focused = els.similarList.closest(".panel")?.classList.contains("focused");
  const width = focused ? 400 : 360;
  const height = focused ? 300 : 300;
  const cx = width / 2;
  const cy = height / 2;
  const outer = 126;
  const nodes = similarity.similar_players;
  const scores = nodes.map((item) => item.score);
  const minScore = scores.length ? Math.min(...scores) : 0;
  const maxScore = scores.length ? Math.max(...scores) : 1;
  const strokeFor = (score) => {
    if (maxScore === minScore) {
      return 5;
    }
    return 1.5 + ((score - minScore) / (maxScore - minScore)) * 7;
  };

  els.similarList.innerHTML = `
    <svg class="network-svg" viewBox="0 0 ${width} ${height}" role="img" aria-label="相似球员网络图">
      ${nodes.map((item, index) => {
        const angle = -Math.PI / 2 + index * Math.PI * 2 / Math.max(nodes.length, 1);
        const radius = outer - item.score * 44;
        const x = cx + Math.cos(angle) * radius;
        const y = cy + Math.sin(angle) * radius;
        return `<line x1="${cx}" y1="${cy}" x2="${x}" y2="${y}" stroke="#d7d0c6" stroke-width="${strokeFor(item.score).toFixed(1)}" stroke-linecap="round" />`;
      }).join("")}
      <circle cx="${cx}" cy="${cy}" r="42" fill="#1f2a2e" />
      <text class="network-center" x="${cx}" y="${cy - 4}" text-anchor="middle">${(player.name || player.player_id).split(" ").slice(-1)[0]}</text>
      <text class="network-sub" x="${cx}" y="${cy + 15}" text-anchor="middle">当前球员</text>
      ${nodes.map((item, index) => {
        const angle = -Math.PI / 2 + index * Math.PI * 2 / Math.max(nodes.length, 1);
        const radius = outer - item.score * 44;
        const x = cx + Math.cos(angle) * radius;
        const y = cy + Math.sin(angle) * radius;
        const r = 18 + item.score * 8;
        return `
          <circle cx="${x}" cy="${y}" r="${r}" fill="rgba(25, 123, 122, 0.92)" stroke="#fff" stroke-width="3" />
          <text class="network-node" x="${x}" y="${y + 4}" text-anchor="middle">${item.name.split(" ").slice(-1)[0]}</text>
          <text class="network-score" x="${x}" y="${y + r + 13}" text-anchor="middle">${focused ? `#${index + 1} · ${Math.round(item.score * 100)}%` : `${Math.round(item.score * 100)}%`}</text>
          ${focused ? `<text class="network-team" x="${x}" y="${y + r + 29}" text-anchor="middle">${item.team || ""}</text>` : ""}
        `;
      }).join("")}
    </svg>
  `;
}

function renderExplanation(explanation) {
  els.explainChart.innerHTML = explanation.contributions.map((item, index) => `
    <div class="bar-row">
      <div class="bar-topline">
        <strong>${zhLabel(item.feature)}</strong>
        <span>${item.value}</span>
      </div>
      <div class="track"><div class="fill ${index === 0 ? "coral" : ""}" style="width:${item.value}%"></div></div>
    </div>
  `).join("");
}

function renderCompare(compare) {
  els.compareTitle.textContent = `${compare.player1_name} 对比 ${compare.player2_name}`;
  const focused = isFocused("comparePanel");
  const entries = Object.entries(compare.diff);
  const maxAbs = Math.max(...entries.map(([, value]) => Math.abs(value)), 1);
  els.compareChart.innerHTML = `
    <div class="compare-head">
      <strong>${compare.player1_name}</strong>
      <span>差值</span>
      <strong>${compare.player2_name}</strong>
    </div>
    ${entries.map(([key, value]) => {
    const width = Math.max(Math.abs(value) / maxAbs * 46, 8);
    const leftWidth = value >= 0 ? width : 0;
    const rightWidth = value < 0 ? width : 0;
    const leader = value >= 0 ? compare.player1_name : compare.player2_name;
    return `
      <div class="compare-duel">
        <span class="compare-label">${zhLabel(key)}</span>
        <div class="duel-track">
          <div class="duel-side duel-left"><i style="width:${leftWidth}%"></i></div>
          <span class="duel-zero"></span>
          <div class="duel-side duel-right"><i style="width:${rightWidth}%"></i></div>
          ${focused ? `<b class="duel-callout ${value >= 0 ? "left" : "right"}">${leader} +${Math.abs(value).toFixed(1)}</b>` : ""}
        </div>
        <strong class="compare-value">${value > 0 ? "+" : ""}${value.toFixed(1)}</strong>
      </div>
    `;
  }).join("")}
  `;
}

async function renderDashboard() {
  const playerId = selectedPlayerId;
  syncCompareSelection();
  setComboValues();
  const compareId = selectedCompareId;
  const [dashboard, compare] = await Promise.all([
    getJson(`${API_BASE}/players/${playerId}/dashboard`),
    getJson(`${API_BASE}/players/compare?player1=${playerId}&player2=${compareId}`)
  ]);
  const compareDashboard = compareId && compareId !== playerId
    ? await getJson(`${API_BASE}/players/${compareId}/dashboard`)
    : null;
  currentDashboard = dashboard;
  currentCompare = compare;
  currentCompareDashboard = compareDashboard;

  renderOverview(dashboard);
  renderVisuals(dashboard, compare, compareDashboard);
}

function clearFocusedPanel() {
  document.querySelectorAll(".panel").forEach((item) => item.classList.remove("focused"));
  document.querySelector(".dashboard")?.classList.remove("focus-mode");
}

function focusPanel(panel) {
  if (!panel?.classList.contains("panel")) {
    panel?.scrollIntoView({ behavior: "smooth", block: "start" });
    return;
  }

  clearFocusedPanel();
  panel.classList.add("focused");
  document.querySelector(".dashboard")?.classList.add("focus-mode");
  panel.scrollIntoView({ behavior: "smooth", block: "center" });
  if (currentDashboard && currentCompare) {
    renderVisuals(currentDashboard, currentCompare, currentCompareDashboard);
  }
}

function initPanelFocus() {
  document.querySelectorAll(".panel").forEach((panel) => {
    panel.addEventListener("click", (event) => {
      if (event.target.closest("input, .combo, select, option, label, a, button")) {
        return;
      }

      const alreadyFocused = panel.classList.contains("focused");
      clearFocusedPanel();

      if (!alreadyFocused) {
        focusPanel(panel);
      } else if (currentDashboard && currentCompare) {
        renderVisuals(currentDashboard, currentCompare, currentCompareDashboard);
      }
    });
  });
}

function initNavFocus() {
  document.querySelectorAll(".nav-list a").forEach((link) => {
    link.addEventListener("click", (event) => {
      const target = document.querySelector(link.getAttribute("href"));
      if (!target) {
        return;
      }
      event.preventDefault();
      focusPanel(target);
    });
  });
}

async function init() {
  try {
    const playerList = await getJson(`${API_BASE}/players`);

    players = playerList;
    players.sort((left, right) => playerLabel(left).localeCompare(playerLabel(right), "en", { sensitivity: "base" }));
    selectedPlayerId = players[0].player_id;
    selectedCompareId = firstOtherPlayerId(selectedPlayerId);
    setComboValues();

    initCombo("player");
    initCombo("compare");
    document.addEventListener("click", (event) => {
      if (!event.target.closest(".combo")) {
        closeCombos();
        setComboValues();
      }
    });
    initPanelFocus();
    initNavFocus();
    await renderDashboard();
  } catch (error) {
    console.error(error);
  }
}

init();
