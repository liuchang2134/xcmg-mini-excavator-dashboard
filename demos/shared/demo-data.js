(function () {
  const models = [
    { id: 'xe19u', model: 'XCMG XE19U', short: 'XE19U', tonnage: '1-2', label: '1-2 吨级', competitors: 11, image: '../assets/arc/xe19u-official-cropped.png', url: '../excavator-1-2t.html', scenes: ['入户庭院', '市政施工', '租赁周转'], focus: '紧凑机身与狭窄空间适应性' },
    { id: 'xe27u', model: 'XCMG XE27U', short: 'XE27U', tonnage: '2-3', label: '2-3 吨级', competitors: 9, image: '../assets/arc/xe27u-official-cropped.jpg', url: '../excavator-2-3t.html', scenes: ['窄场地', '沟槽施工', '属具适配'], focus: '短尾回转与运输便利性' },
    { id: 'xe35u', model: 'XCMG XE35U', short: 'XE35U', tonnage: '3-4', label: '3-4 吨级', competitors: 10, image: '../assets/arc/xe35u-official-cropped.jpg', url: '../index.html', scenes: ['狭窄空间', '短循环', '破碎作业'], focus: '多工况能力与配置完整度' },
    { id: 'xe45u', model: 'XCMG XE45U', short: 'XE45U', tonnage: '4-5', label: '4-5 吨级', competitors: 7, image: '../assets/arc/xe45u-official-cropped.png', url: '../excavator-4-5t.html', scenes: ['运输边界', '沟槽施工', '租赁应用'], focus: '运输边界与作业覆盖' },
    { id: 'xe55u', model: 'XCMG XE55U', short: 'XE55U', tonnage: '5-6', label: '5-6 吨级', competitors: 10, image: '../assets/arc/xe55u-official-cropped.jpg', url: '../excavator-5-6t.html', scenes: ['土方装车', '液压属具', '驾驶安全'], focus: '装车效率与液压属具能力' },
    { id: 'xe75u', model: 'XCMG XE75U', short: 'XE75U', tonnage: '7-8', label: '7-8 吨级', competitors: 6, image: '../assets/arc/xe75u-official-cropped.jpg', url: '../excavator-7-8t.html', scenes: ['沟槽深挖', '坡地作业', '吊装'], focus: '深挖、稳定性与吊装能力' },
    { id: 'xe80u', model: 'XCMG XE80U', short: 'XE80U', tonnage: '8-10', label: '8-10 吨级', competitors: 9, image: '../assets/arc/xe80u-official-cropped.jpg', url: '../excavator-8-10t.html', scenes: ['市政土方', '深挖', '破碎作业'], focus: '中型施工效率与配置组合' },
    { id: 'xe135u', model: 'XCMG XE135U', short: 'XE135U', tonnage: '12-14', label: '12-14 吨级', competitors: 9, image: '../assets/arc/xe135u-official-cropped.webp', url: '../excavator-12-14t.html', scenes: ['土方装车', '沟槽', '公路施工'], focus: '生产率与燃油效率平衡' },
    { id: 'xe155ucr', model: 'XCMG XE155UCR', short: 'XE155UCR', tonnage: '14-16', label: '14-16 吨级短尾', competitors: 9, image: '../assets/arc/xe155ucr-official-cropped.jpg', url: '../excavator-14-16t-short-tail.html', scenes: ['短尾回转', '受限空间', '装车'], focus: '受限场地中的中型作业能力' },
    { id: 'xe225u', model: 'XCMG XE225U', short: 'XE225U', tonnage: '21-24', label: '21-24 吨级', competitors: 9, image: '../assets/arc/xe225u-official-cropped.png', url: '../excavator-21-24t.html', scenes: ['重载土方', '深挖', '破碎作业'], focus: '重载生产率与耐久性' }
  ];

  const lines = [
    { id: 'excavators', en: 'Excavators', zh: '挖掘机', image: '../assets/arc/category-excavators.jpg', status: '已接入', live: true, scope: '10 个吨级资产' },
    { id: 'wheel-loaders', en: 'Wheel Loaders', zh: '装载机', image: '../assets/arc/category-wheel-loaders-clean.jpg', status: '待接入', live: false, scope: '装载效率与油耗' },
    { id: 'rollers', en: 'Rollers', zh: '压路机', image: '../assets/arc/category-rollers.jpeg', status: '待接入', live: false, scope: '压实与振动性能' },
    { id: 'motor-graders', en: 'Motor Graders', zh: '平地机', image: '../assets/arc/category-motor-graders.webp', status: '待接入', live: false, scope: '精度、牵引与控制' },
    { id: 'cranes', en: 'Cranes', zh: '起重机械', image: '../assets/arc/category-cranes.webp', status: '待接入', live: false, scope: '载荷曲线与安全系统' },
    { id: 'haul-trucks', en: 'Haul Trucks', zh: '矿用卡车', image: '../assets/arc/category-haul-trucks.webp', status: '待接入', live: false, scope: '载重与循环效率' },
    { id: 'mewp', en: 'MEWP', zh: '高空作业平台', image: '../assets/arc/category-mewp-clean.jpg', status: '待接入', live: false, scope: '作业高度与租赁适配' }
  ];

  window.XCMG_DEMO = {
    models,
    lines,
    getModel(id) { return models.find((item) => item.id === id) || models[0]; },
    getLine(id) { return lines.find((item) => item.id === id) || lines[0]; },
    competitorTotal: models.reduce((sum, item) => sum + item.competitors, 0)
  };
}());
