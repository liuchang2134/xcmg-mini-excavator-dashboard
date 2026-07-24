(function () {
  'use strict';

  const query = new URLSearchParams(window.location.search);
  let storedLanguage = '';
  try { storedLanguage = window.localStorage.getItem('xcmg-benchmark-language') || ''; } catch (_) { storedLanguage = ''; }
  const language = query.get('lang') === 'en' || (query.get('lang') !== 'zh' && storedLanguage === 'en') ? 'en' : 'zh';
  const locale = language === 'en' ? 'en-US' : 'zh-CN';

  const copy = {
    zh: {
      actual: '历史实际',
      forecast: '历史预测',
      plan: '历史规划',
      units: '台',
      sourcePeriod: '原时间口径',
      marketCycle: '北美挖掘机市场周期',
      cycleRead: '周期判断',
      cycleText: '政策刺激和车队补库把市场推至 2023 年高点；随后融资成本、渠道库存和终端建设需求共同促使销量回调。2024 年仍有 98,632 台，但较 2023 年高点低 25.3%。这意味着产品竞争不能只讲采购价格，还要证明设备周转、小时产量、停机风险和残值。',
      demandDirection: '需求方向',
      demandText: '微小挖仍受城市更新、住宅后院、市政公用事业和租赁周转支撑；中大挖则更多依赖基础设施、土方、道路、矿山和专业承包商。南部及东南部人口增长州适合集中开展样机投放、属具验证和用户诊断。',
      financeImpact: '融资与租赁',
      financeText: '高利率会抬高设备月供和经销库存成本，租赁客户因此更加关注跨客户通用性、非专业机手适应性、保养周转和二手机价值。主机、属具、金融和服务不能分开设计。',
      mixTitle: '2019–2024 挖掘机产品结构',
      mixSubtitle: 'EDA 融资交易占比',
      tonnageMovement: '2024 各吨级销量与同比变化',
      tonnageExplanation: '颜色表示 2023–2024 销量调整幅度，不表示产品性能。重点规格同时考虑市场体量、应用广度和现有型谱角色。',
      competitionCompact: '0–10 吨微小挖',
      competitionLarge: '10 吨以上中大挖',
      compactConcentration: '前四品牌合计 74%',
      largeConcentration: '前三品牌合计 69%',
      brandUnits: '销量',
      brandShare: '份额',
      fieldMatrix: '工况—产品能力矩阵',
      portfolioMatrix: 'XCMG 产品型谱覆盖矩阵',
      issueMap: '跨产品问题主题分布',
      issueCount: '条目数只表示被记录的改进事项数量，不代表严重程度。',
      ledgerTitle: '重点机型问题与工程动作',
      targetTitle: '历史销量规划路径',
      targetNote: '2025–2027 为历史目标，不代表当前实际销量或已批准预测。',
      dataBasis: '分析口径',
      dataBasisText: '市场结构采用 AEM 与 EDA 的原时间段数据；工况和客户判断来自经销、租赁、终端及工程观察；产品差距需要以当前量产配置、受控试验和北美实机验证更新。'
    },
    en: {
      actual: 'Historical actual',
      forecast: 'Historical forecast',
      plan: 'Historical plan',
      units: 'units',
      sourcePeriod: 'Original time basis',
      marketCycle: 'North American excavator market cycle',
      cycleRead: 'Cycle interpretation',
      cycleText: 'Policy stimulus and fleet restocking pushed the market to a 2023 peak. Financing costs, channel inventory and softer end demand then drove a correction. The 2024 volume remained 98,632 units but was 25.3% below the peak. Product competition therefore has to prove utilization, hourly output, downtime risk and residual value rather than acquisition price alone.',
      demandDirection: 'Demand direction',
      demandText: 'Mini and compact excavators continue to serve urban renewal, residential backyards, municipal utilities and rental turnover. Medium and large machines depend more on infrastructure, earthmoving, roads, quarry work and professional contractors. Fast-growing southern and southeastern states are logical priorities for prototype placement, attachment validation and user clinics.',
      financeImpact: 'Finance and rental',
      financeText: 'Higher interest rates increase monthly ownership cost and dealer inventory expense. Rental customers therefore place more value on multi-customer versatility, novice-operator usability, service turnaround and used-equipment value. Machine, attachment, finance and support packages must be designed together.',
      mixTitle: '2019-2024 excavator product mix',
      mixSubtitle: 'Share of EDA financed transactions',
      tonnageMovement: '2024 volume and year-on-year movement by class',
      tonnageExplanation: 'Color describes the 2023-2024 market correction, not product performance. Priority classes also reflect volume, application breadth and the role of the current portfolio.',
      competitionCompact: 'Mini and compact, 0-10 t',
      competitionLarge: 'Medium and large, above 10 t',
      compactConcentration: 'Top four brands: 74%',
      largeConcentration: 'Top three brands: 69%',
      brandUnits: 'Units',
      brandShare: 'Share',
      fieldMatrix: 'Application-to-capability matrix',
      portfolioMatrix: 'XCMG product portfolio coverage',
      issueMap: 'Cross-product issue-theme distribution',
      issueCount: 'Counts describe documented improvement items, not severity.',
      ledgerTitle: 'Priority model gaps and engineering actions',
      targetTitle: 'Historical sales-planning path',
      targetNote: '2025-2027 values are historical targets, not current actuals or approved forecasts.',
      dataBasis: 'Analysis basis',
      dataBasisText: 'Market structure retains the original AEM and EDA periods. Application and customer findings combine dealer, rental, end-user and engineering observations. Product gaps must be refreshed using current production configuration, controlled tests and North American field validation.'
    }
  }[language];

  const regionalSignals = [
    {
      region: {zh: '南部与东南部增长州', en: 'Growing South and Southeast'},
      states: 'TX · FL · NC · GA · SC · TN',
      demand: {
        zh: '人口迁移和住房、公用事业、市政道路扩张，推动沟槽、景观、场地整理、管线和小型土方需求。',
        en: 'Population migration and expansion in housing, utilities and municipal roads support trenching, landscaping, grading, pipe work and compact earthmoving.'
      },
      response: {
        zh: '优先布置 1–10 吨样机与多属具包，在高温、红土、潮湿和高周转条件下验证散热、密封、履带、液压和维护周转。',
        en: 'Prioritize 1-10 t prototypes and multi-attachment packages, validating cooling, sealing, undercarriage, hydraulics and service turnaround in heat, red soil, humidity and high-utilization duty.'
      }
    },
    {
      region: {zh: '城市更新与高密度区域', en: 'Urban renewal and dense sites'},
      states: {zh: '东北部 · 大湖区 · 西海岸城市带', en: 'Northeast · Great Lakes · West Coast metros'},
      demand: {
        zh: '道路翻修、地下设施、住宅改造和拆除任务强调短尾、低噪、运输包络、视野与精细复合动作。',
        en: 'Road repair, underground utilities, residential renovation and demolition emphasize short-tail packaging, low noise, transport envelope, visibility and precise combined motion.'
      },
      response: {
        zh: '用短尾产品、快换、破碎锤、抓具、倾转属具和全景影像组成城市施工包，并验证回转制动与贴边作业稳定性。',
        en: 'Build an urban package around short-tail machines, couplers, hammers, grapples, tilt attachments and surround-view cameras, then validate swing braking and close-wall stability.'
      }
    },
    {
      region: {zh: '基础设施、土方与矿山带', en: 'Infrastructure, earthmoving and quarry regions'},
      states: {zh: '跨州道路 · 工业项目 · 采石场与矿区', en: 'Interstate roads · industrial projects · quarries and mines'},
      demand: {
        zh: '中大挖更看重小时产量、油耗、装车循环、起吊、深挖、耐久、运输拆装与服务保障。',
        en: 'Medium and large excavators are judged on hourly output, fuel use, loading cycle, lifting, digging depth, durability, transport preparation and support coverage.'
      },
      response: {
        zh: '通过长斗杆、大斗容、重载底盘、宽履带、可拆配重和智能辅助形成工况包，并以吨/小时、升/小时和开工率验证。',
        en: 'Build application packages with long sticks, larger buckets, heavy-duty undercarriages, wider shoes, removable counterweights and grade assistance, then validate tonnes per hour, litres per hour and uptime.'
      }
    }
  ];

  const customerSegments = [
    {
      segment: {zh: '个体机主与小型承包商', en: 'Owner-operators and small contractors'},
      work: {zh: '住宅、景观、排水、围栏、基础维修；任务多变，设备通常由同一人运输、操作和维护。', en: 'Residential, landscaping, drainage, fencing and foundation repair; one person often transports, operates and services the machine.'},
      decision: {zh: '易运输、易学、故障少、属具切换快、经销响应快，月供和二手机价值直接影响购买。', en: 'Transportability, easy learning, low failure risk, fast attachment changes and dealer response matter; monthly payment and resale value directly affect purchase.'},
      product: {zh: '微小挖应把整备质量、尾部形式、快换、AUX 流量、日常保养点和驾驶舒适性作为一个完整方案。', en: 'Mini machines need one integrated package covering equipped mass, tail format, coupler, auxiliary flow, daily service points and operator comfort.'}
    },
    {
      segment: {zh: '租赁公司', en: 'Rental companies'},
      work: {zh: '跨客户、跨机手、跨属具高频周转，设备必须适应不稳定的操作水平和短租任务。', en: 'High-frequency turnover across customers, operators and attachments requires tolerance for uneven skill levels and short-duration jobs.'},
      decision: {zh: '利用率、停机时间、损坏风险、统一附件、远程管理、保养时间和残值优先于单一峰值参数。', en: 'Utilization, downtime, damage risk, attachment commonality, telematics, service time and residual value outweigh one peak specification.'},
      product: {zh: '形成租赁配置包：防误操作、自动停机、报警管理、快换兼容、关键部位防护、远程定位和标准化交机培训。', en: 'Create a rental package with misuse protection, auto idle/shutdown, alarm management, coupler compatibility, guarding, telematics and standardized handover training.'}
    },
    {
      segment: {zh: '市政、公用事业与道路承包商', en: 'Municipal, utility and road contractors'},
      work: {zh: '沟槽、管线、道路维修、桥梁周边、回填和起吊，常在交通和人员附近作业。', en: 'Trenching, pipe work, road repair, bridge approaches, backfilling and lifting often occur near traffic and people.'},
      decision: {zh: '工作范围、起吊能力、回转包络、稳定性、视野、报警、辅助挖掘和快速维修决定中标与施工效率。', en: 'Working range, lift capacity, swing envelope, stability, visibility, alarms, grade assistance and rapid repair affect both bid suitability and productivity.'},
      product: {zh: '短尾与常规尾需并行，按沟槽深度、管径、道路宽度和吊装重量配置斗杆、配重、履带、影像与坡度系统。', en: 'Short-tail and conventional-tail variants should coexist, with stick, counterweight, track, camera and grade-system choices tied to trench depth, pipe diameter, road width and lift load.'}
    },
    {
      segment: {zh: '大型土方、矿山与专业车队', en: 'Large earthmoving, quarry and professional fleets'},
      work: {zh: '长时间装车、剥离、采石、深挖和大批量土方，强调连续循环与计划停机管理。', en: 'Long-duration loading, stripping, quarry, deep excavation and bulk earthmoving emphasize continuous cycles and planned downtime.'},
      decision: {zh: '小时产量、燃油效率、耐久、可维修性、配件保障、金融、回购和残值共同决定全生命周期成本。', en: 'Hourly output, fuel efficiency, durability, serviceability, parts coverage, finance, buyback and residual value jointly determine lifecycle cost.'},
      product: {zh: '中大挖必须用完整生产率试验和耐久记录说话，同时提供重载斗、长斗杆、宽履带、可拆配重和远程车队管理。', en: 'Medium and large machines require full productivity tests and durability records, supported by heavy-duty buckets, long sticks, wide shoes, removable counterweights and fleet telematics.'}
    }
  ];

  const macroSignals = [
    {
      factor: {zh: '社会与区域', en: 'Social and regional'},
      signal: {zh: '人口向德州、佛州、北卡、佐治亚州、南卡和田纳西州等增长州迁移，住宅与基础设施需求随之转移。', en: 'Population movement toward Texas, Florida, the Carolinas, Georgia and Tennessee shifts residential and infrastructure demand.'},
      impact: {zh: '区域样机、经销备件和属具验证应跟着施工活动走，而不是平均分配资源。', en: 'Prototype fleets, dealer parts and attachment validation should follow construction activity rather than be spread evenly.'}
    },
    {
      factor: {zh: '技术', en: 'Technology'},
      signal: {zh: '高端化、智能化和低排放方向持续，但客户更在意功能是否经过本地工况标定。', en: 'Premium, intelligent and lower-emission technologies continue, but customers care whether functions are tuned for local applications.'},
      impact: {zh: '优先做好液压标定、坡度辅助、远程诊断、全景影像和清晰的人机交互，避免只堆叠功能名称。', en: 'Prioritize hydraulic calibration, grade assistance, remote diagnostics, surround view and clear HMI instead of merely adding feature names.'}
    },
    {
      factor: {zh: '经济与租赁', en: 'Economy and rental'},
      signal: {zh: '市场从补库存高点进入调整期，高利率推高月供和经销库存成本，租赁仍是重要需求渠道。', en: 'The market moved from a restocking peak into adjustment; high rates raise payments and dealer inventory cost while rental remains a major channel.'},
      impact: {zh: '整机要证明利用率、停机风险、保养效率和残值，金融与租赁包应进入产品定义。', en: 'Machines must prove utilization, downtime risk, service efficiency and residual value; finance and rental packages belong in product definition.'}
    },
    {
      factor: {zh: '环境与排放', en: 'Environment and emissions'},
      signal: {zh: '加州激励与其他州的支持强度不同，电动化采用速度受法规、补能条件和任务周期约束。', en: 'California incentives and support in other states differ; electrification depends on regulation, charging conditions and duty cycle.'},
      impact: {zh: '新能源产品按州、客户和工况分层导入，同时保留极寒、高温、粉尘和腐蚀环境适应性验证。', en: 'Stage electrified products by state, customer and duty cycle while retaining cold, heat, dust and corrosion validation.'}
    },
    {
      factor: {zh: '贸易与准入', en: 'Trade and market access'},
      signal: {zh: '关税、认证、反倾销风险与本地采购要求会影响落地成本、交付路径和配置选择。', en: 'Tariffs, certification, trade-remedy risk and local-content requirements affect landed cost, delivery paths and configuration choices.'},
      impact: {zh: '产品配置、友岸保供、零部件本地化和认证替代方案需同步评估，避免只看出厂成本。', en: 'Configuration, allied sourcing, component localization and certification alternatives must be evaluated together rather than using factory cost alone.'}
    }
  ];

  const scenarios = [
    {
      image: 'assets/ppt-insights/excavator-1-2t-02.webp',
      className: '1–2 t',
      title: {zh: '住宅后院与贴边施工', en: 'Backyard and close-wall work'},
      customer: {zh: '景观承包商、租赁客户、小型施工队', en: 'Landscapers, rental users and small crews'},
      narrative: {zh: '设备需穿过狭窄通道并在建筑、围栏和硬化地面附近完成挖沟、拆除和回填。真正的约束不是名义吨位，而是收缩宽度、尾部回转、动臂偏摆、视野、低速微操和地面保护。', en: 'The machine must pass through narrow access and trench, demolish or backfill beside buildings, fences and finished surfaces. The real constraints are retractable width, tail swing, boom offset, visibility, low-speed control and ground protection rather than nominal tonnage.'}
    },
    {
      image: 'assets/ppt-insights/excavator-2-3t-03.webp',
      className: '2–3 t',
      title: {zh: '市政拆除与多属具切换', en: 'Municipal demolition and attachment changes'},
      customer: {zh: '市政承包商、道路维修与租赁公司', en: 'Municipal contractors, road repair and rental fleets'},
      narrative: {zh: '破碎、抓取、装车和清理会在同一工地连续发生。快换兼容、AUX 流量、管路防护、破碎锤标定、回转制动和非专业机手适应性共同决定设备是否真正通用。', en: 'Hammering, grabbing, loading and cleanup can occur sequentially on one site. Coupler compatibility, auxiliary flow, hose protection, hammer calibration, swing braking and novice-operator usability jointly determine true versatility.'}
    },
    {
      image: 'assets/ppt-insights/excavator-35t-01.webp',
      className: '3–4 t',
      title: {zh: '城市道路与受限破碎', en: 'Urban roadwork and confined hammering'},
      customer: {zh: '市政、公用事业和小型承包商', en: 'Municipal, utility and small contractors'},
      narrative: {zh: '在人车混行环境中，设备需要兼顾运输、短尾包络、贴边作业、报警、后方视野和破碎效率。驾驶室/驾驶棚、后视摄像头、坡度系统和不同尾型必须按任务组合，不能只用一个配置覆盖所有客户。', en: 'Around traffic and pedestrians, the machine must balance transport, short-tail envelope, close-wall work, alarms, rear visibility and hammer productivity. Cab/canopy, rear camera, grade system and tail configuration must be packaged by task rather than treated as one universal specification.'}
    },
    {
      image: 'assets/ppt-insights/excavator-5-6t-01.webp',
      className: '5–6 t',
      title: {zh: '基础沟槽与回填整平', en: 'Foundation trenching and backfill'},
      customer: {zh: '基础承包商、住宅施工和公用事业', en: 'Foundation contractors, residential builders and utilities'},
      narrative: {zh: '连续挖沟、转场、回填和整平要求工作范围、行走速度、推土铲控制、回转效率和 AUX 能力保持平衡。斗杆过短、行走慢或推土铲交互不顺都会在一个完整工作日内累积成明显产能差。', en: 'Repeated trenching, repositioning, backfilling and grading require balance among working range, travel speed, blade control, swing efficiency and auxiliary capability. A short stick, slow travel or awkward blade controls accumulate into a material daily productivity gap.'}
    },
    {
      image: 'assets/ppt-insights/excavator-12-16t-02.webp',
      className: '12–16 t',
      title: {zh: '公用事业与道路管线', en: 'Utility and road-side pipe work'},
      customer: {zh: '公用事业、道路承包商和市政部门', en: 'Utilities, road contractors and municipalities'},
      narrative: {zh: '道路开挖和管线任务把沟槽深度、管径、吊装重量、交通净空和回填精度放在同一工况中。短尾、长斗杆、起吊图表、坡度辅助、摄像头和稳定底盘需要按项目组合。', en: 'Road excavation and utility work combine trench depth, pipe diameter, lift load, traffic clearance and backfill precision. Short tail, long stick, lift charts, grade assist, cameras and a stable undercarriage must be packaged by project.'}
    },
    {
      image: 'assets/ppt-insights/excavator-19-24t-01.webp',
      className: '19–24 t',
      title: {zh: '住宅开发与批量土方', en: 'Residential development and bulk earthmoving'},
      customer: {zh: '场地开发商、基础承包商和土方车队', en: 'Site developers, foundation contractors and earthmoving fleets'},
      narrative: {zh: '挖装、平地、起吊和转场频繁交替，客户关注斗容、循环时间、回转力矩、挖掘力、燃油效率和驾驶室连续作业舒适性。该吨级必须通过生产率试验，而不是仅靠纸面参数判断。', en: 'Digging, loading, grading, lifting and repositioning alternate frequently. Customers focus on bucket capacity, cycle time, swing torque, digging force, fuel efficiency and all-day cab comfort. This class requires productivity testing rather than specification-only judgment.'}
    },
    {
      image: 'assets/ppt-insights/excavator-33-40t-04.webp',
      className: '33–40 t',
      title: {zh: '采石场与重载挖装', en: 'Quarry and heavy excavation'},
      customer: {zh: '采石场、骨料企业和重型土方承包商', en: 'Quarries, aggregate producers and heavy earthmoving contractors'},
      narrative: {zh: '岩石、坡面和装车循环对结构耐久、铲斗/斗杆挖掘力、回转力矩、底盘稳定、散热、防尘和维修可达性提出更高要求。每小时产量和停机风险比采购价更直接影响客户决策。', en: 'Rock, slopes and loading cycles raise requirements for structural durability, bucket/stick force, swing torque, undercarriage stability, cooling, dust protection and service access. Hourly output and downtime risk influence the decision more directly than acquisition price.'}
    },
    {
      image: 'assets/ppt-insights/excavator-40-60t-01.webp',
      className: '40–60 t',
      title: {zh: '大型土方装车与运输组织', en: 'Large loading and transport planning'},
      customer: {zh: '大型土方、矿山和基础设施项目', en: 'Large earthmoving, mining and infrastructure projects'},
      narrative: {zh: '大斗容装车、深挖和重载循环需要把工作装置、回转、起吊、履带、配重和运输拆装作为一个系统评估。运输高度、履带宽度、可拆配重和引导车成本会直接改变设备的项目经济性。', en: 'Large-bucket loading, deep excavation and heavy cycles require a system view of front attachment, swing, lifting, tracks, counterweight and transport preparation. Transport height, shoe width, removable counterweight and escort cost directly change project economics.'}
    }
  ];

  const capabilityMatrix = [
    {scenario: {zh: '狭窄住宅与景观', en: 'Confined residential and landscaping'}, packaging: '●', range: '●', hydraulics: '●', attachments: '●', stability: '○', visibility: '●', service: '○'},
    {scenario: {zh: '市政沟槽与公用事业', en: 'Municipal trenching and utilities'}, packaging: '●', range: '●', hydraulics: '●', attachments: '●', stability: '●', visibility: '●', service: '●'},
    {scenario: {zh: '租赁与多客户周转', en: 'Rental and multi-customer turnover'}, packaging: '●', range: '○', hydraulics: '●', attachments: '●', stability: '●', visibility: '●', service: '●'},
    {scenario: {zh: '破碎、拆除与多属具', en: 'Hammering, demolition and attachments'}, packaging: '○', range: '●', hydraulics: '●', attachments: '●', stability: '●', visibility: '●', service: '●'},
    {scenario: {zh: '批量土方与装车', en: 'Bulk earthmoving and loading'}, packaging: '○', range: '●', hydraulics: '●', attachments: '●', stability: '●', visibility: '○', service: '●'},
    {scenario: {zh: '采石场与矿山重载', en: 'Quarry and mining duty'}, packaging: '○', range: '●', hydraulics: '●', attachments: '●', stability: '●', visibility: '●', service: '●'}
  ];

  const benchmarkRows = [
    {
      dimension: {zh: '产品性能', en: 'Product performance'},
      kubota: {zh: '微操与复合动作细腻，短尾/常规尾和高低配覆盖成熟。', en: 'Fine control and combined motion, with mature short-tail/conventional-tail and trim coverage.'},
      xcmgMini: {zh: '节能基础具备，但微操响应、复合动作协调和细节工艺仍需持续验证。', en: 'Efficiency foundations exist, but fine response, combined-motion coordination and detail quality need continued validation.'},
      cat: {zh: '电液控制、智能辅助、重载平台和应用配置处于中大挖标杆水平。', en: 'Electrohydraulics, intelligent assistance, heavy-duty platforms and application packages define the mid/large benchmark.'},
      xcmgLarge: {zh: '需补强操控、可靠性、智能化、生产率与平台化配置。', en: 'Control, reliability, intelligence, productivity and platformized options require strengthening.'}
    },
    {
      dimension: {zh: '客户与定位', en: 'Customer and positioning'},
      kubota: {zh: '中小承包商与租赁客户认可度高，强调易用、稳定和高残值。', en: 'Strong recognition among small contractors and rental customers, emphasizing usability, stability and residual value.'},
      xcmgMini: {zh: '成本有潜力，但品牌认知、使用口碑和持续服务仍在建立。', en: 'Cost position has potential, while brand familiarity, operating reputation and support consistency are still being built.'},
      cat: {zh: '专业车队把 CAT 作为性能、可靠性和拥有成本的参照。', en: 'Professional fleets use CAT as a reference for performance, reliability and ownership cost.'},
      xcmgLarge: {zh: '只有产品力和服务达到门槛后，价格差才能转化为价值优势。', en: 'Only after product and support reach the threshold can price position become a value advantage.'}
    },
    {
      dimension: {zh: '商务与后市场', en: 'Commercial and aftermarket'},
      kubota: {zh: '融资、延保、保养周期、快速服务和二手机价值形成闭环。', en: 'Finance, extended warranty, service intervals, rapid support and used value form a closed loop.'},
      xcmgMini: {zh: '质保基础较长，但融资灵活度、配件响应和残值体系需继续完善。', en: 'Warranty coverage is a foundation, but finance flexibility, parts response and residual-value systems need improvement.'},
      cat: {zh: '金融、租赁、回购、再制造、配件与 24/7 服务构成完整体系。', en: 'Finance, rental, buyback, remanufacturing, parts and 24/7 support form one integrated system.'},
      xcmgLarge: {zh: '需要把主机改进与服务网络、备件时效和 TCO 证明同步推进。', en: 'Machine improvement must advance with service coverage, parts lead time and TCO evidence.'}
    }
  ];

  const officialPortfolio = [
    {range: '1–2 t', model: 'XE19U', image: 'assets/arc/xe19u-official-cropped.png', role: {zh: '微挖运输与狭窄作业', en: 'Mini transport and confined work'}},
    {range: '3–4 t', model: 'XE35U', image: 'assets/arc/xe35u-official-cropped.jpg', role: {zh: '微挖核心规格', en: 'Core mini class'}},
    {range: '5–6 t', model: 'XE55U', image: 'assets/arc/xe55u-official-cropped.jpg', role: {zh: '小挖通用施工', en: 'Compact general construction'}},
    {range: '12–14 t', model: 'XE135U', image: 'assets/arc/xe135u-official-cropped.webp', role: {zh: '中挖基础与公用工程', en: 'Medium foundations and utilities'}},
    {range: '21–24 t', model: 'XE225U', image: 'assets/arc/xe225u-official-cropped.png', role: {zh: '主流土方与装车', en: 'Mainstream earthmoving and loading'}},
    {range: '33–40 t', model: 'XE360U', image: 'assets/arc/xe360u-official-cropped.webp', role: {zh: '大型土方与重载', en: 'Large earthmoving and heavy duty'}},
    {range: '40–60 t', model: 'XE490U', image: 'assets/arc/xe490u-official.jpg', role: {zh: '大型装车与矿山', en: 'Large loading and quarry duty'}}
  ];

  const issueThemeLabels = {
    transport: {zh: '运输包络', en: 'Transport'},
    travel: {zh: '行走', en: 'Travel'},
    work_equipment: {zh: '工作装置', en: 'Work equipment'},
    hydraulics: {zh: '液压与属具', en: 'Hydraulics'},
    swing_control: {zh: '回转控制', en: 'Swing control'},
    stability: {zh: '稳定与起吊', en: 'Stability'},
    cab_hmi: {zh: '驾驶室与 HMI', en: 'Cab and HMI'},
    vision: {zh: '视野与影像', en: 'Visibility'},
    service: {zh: '维修便利', en: 'Serviceability'}
  };

  const detailedLedger = [
    {
      model: 'XE18U / XE19U',
      gaps: {zh: '行走报警不能主动消音、行走速度偏慢、回转制动与脚踏线性仍需优化，驾驶室便利配置不足。', en: 'Travel alarm muting, travel speed, swing braking and pedal linearity required improvement, together with cab convenience items.'},
      action: {zh: '以更高功率平台、行走马达与脚踏标定、回转制动方案和交机配置包进行验证。', en: 'Validate a higher-power platform, travel motor and pedal calibration, swing-brake solution and delivery package.'},
      validation: {zh: '核对当前 XE19U 量产配置与北美客户试用结果。', en: 'Confirm current XE19U production configuration and North American customer-trial results.'}
    },
    {
      model: 'XE35U',
      gaps: {zh: '整备质量、运输余量、四向/浮动推土铲、行走稳定、挖掘力、AUX 流量、回转制动、维修加注和显示交互形成一组系统性差距。', en: 'Equipped mass, transport margin, 4-way/float blade, travel stability, digging force, auxiliary flow, swing braking, service filling and display interaction form a systemic gap set.'},
      action: {zh: '建立轻量化包络，重做底盘与推土铲功能边界，联合优化主泵、阀控、回转和工作装置，并形成安全与租赁配置包。', en: 'Define a lightweight envelope, reset undercarriage and blade boundaries, jointly optimize pump, valve, swing and front attachment, and create safety and rental packages.'},
      validation: {zh: '用运输组合、循环作业、行走启停和多属具试验形成同一份验证报告。', en: 'Use one validation report covering transport combination, duty cycles, travel start/stop and multiple attachments.'}
    },
    {
      model: 'XE55U',
      gaps: {zh: '发动机与系统功率、行走速度和牵引力、铲斗挖掘力、推土铲交互、维修加注、侧门操作和后方视野均出现差距。', en: 'Engine/system power, travel speed and traction, bucket force, blade interaction, service filling, side-door operation and rear visibility all showed gaps.'},
      action: {zh: '动力、主泵、行走马达与铲斗力需联合匹配；同时把手柄控制、后视影像、报警消音和维修口纳入标准配置审核。', en: 'Match engine, main pump, travel motor and bucket force together, while reviewing control integration, rear camera, alarm muting and service port as standard equipment.'},
      validation: {zh: '以典型沟槽、坡地转场、租赁周转和属具作业测量效率与油耗。', en: 'Measure productivity and fuel use in trenching, slope travel, rental turnover and attachment work.'}
    },
    {
      model: 'XE80U',
      gaps: {zh: '运输高度、整机质量、双动臂稳定性、高低速与推土铲控制分离、液压油加注便利性影响施工与维护。', en: 'Transport height, operating mass, two-piece-boom stability, separated travel/blade controls and hydraulic-oil filling affect work and service.'},
      action: {zh: '降高设计、底盘与配重选项、控制集成和独立加注口应作为同一代际升级验证。', en: 'Height reduction, undercarriage/counterweight options, control integration and a dedicated fill port should be validated as one generation update.'},
      validation: {zh: '检查运输净空、接地比压、稳定边界与维护时间，避免单项优化引入新问题。', en: 'Check transport clearance, ground pressure, stability envelope and service time so one improvement does not create another issue.'}
    },
    {
      model: 'XE225U / XE235UCR',
      gaps: {zh: '长斗杆与工作范围、回转制动和力矩、挖掘力、管路包络、驾驶室空间、影像/辅助挖掘与脚阀线性需要按常规尾和短尾分别验证。', en: 'Long-stick range, swing braking and torque, digging force, hose envelope, cab space, camera/grade assistance and pedal linearity need separate validation for conventional and short-tail machines.'},
      action: {zh: '围绕沟槽、土方装车和市政受限空间建立两套工况包，明确斗杆、管路、配重、影像和液压标定边界。', en: 'Build two application packages around trenching/bulk loading and municipal confined work, defining stick, hose, counterweight, camera and hydraulic-calibration boundaries.'},
      validation: {zh: '采用同场地同机手循环测试与起吊图表复核。', en: 'Use same-site, same-operator cycle testing and lift-chart verification.'}
    },
    {
      model: 'XE360U',
      gaps: {zh: '稳定性、动臂速度、运输高度、标配斗容、自动双速、回转力矩、辅助挖掘、显示器和脚阀线性共同影响重载效率。', en: 'Stability, boom speed, transport height, standard bucket capacity, auto two-speed, swing torque, grade assistance, display and pedal linearity jointly affect heavy-duty productivity.'},
      action: {zh: '按大土方装车工况联合定义加长底盘、配重、大斗容、回转系统和智能辅助配置。', en: 'Jointly define longer undercarriage, counterweight, larger bucket, swing system and intelligent assistance for bulk-loading duty.'},
      validation: {zh: '以装车循环、吨/小时、升/小时、坡地稳定和运输准备时间进行对标。', en: 'Benchmark loading cycle, tonnes per hour, litres per hour, slope stability and transport-preparation time.'}
    },
    {
      model: 'XE490U',
      gaps: {zh: '运输高度、履带宽度、配重拆装、斗容、回转力矩、动臂速度、起吊稳定、显示与全景影像构成大型设备系统差距。', en: 'Transport height, shoe width, counterweight removal, bucket capacity, swing torque, boom speed, lift stability, display and surround view form a system-level gap on the large machine.'},
      action: {zh: '围绕 4 m³ 级装车、深沟、重载起吊和跨州运输定义不同配置包，不能用单一基础机型覆盖。', en: 'Define separate packages for approximately 4 m³ loading, deep trenching, heavy lifting and interstate transport rather than using one base configuration.'},
      validation: {zh: '以运输许可成本、装车循环、起吊曲线、冷却与连续作业可靠性综合判断。', en: 'Evaluate transport-permit cost, loading cycle, lift curve, cooling and continuous-duty reliability together.'}
    }
  ];

  function text(value) {
    if (value == null) return '';
    if (typeof value === 'object') return value[language] || value.zh || value.en || '';
    return String(value);
  }

  function esc(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function formatNumber(value) {
    return Number(value).toLocaleString(locale);
  }

  function setHtml(selector, html) {
    const element = document.querySelector(selector);
    if (element) element.innerHTML = html;
  }

  function renderSummary(data) {
    const compactUnits = data.competition_2025.compact.find((item) => item.brand === 'XCMG')?.units || 0;
    const largeUnits = data.competition_2025.mid_large.find((item) => item.brand === 'XCMG')?.units || 0;
    const kpis = language === 'en'
      ? [
        ['2024 market volume', '98,632', 'AEM historical actual'],
        ['Mini + compact mix', '77%', '2024 financed-transaction structure'],
        ['Documented 2025 XCMG volume', formatNumber(compactUnits + largeUnits), `${formatNumber(compactUnits)} units at 0-10 t + ${formatNumber(largeUnits)} above 10 t`],
        ['Historical portfolio coverage', '75% / 78%', 'Mini/compact / medium/large']
      ]
      : [
        ['2024 市场规模', '98,632', 'AEM 历史实际'],
        ['微挖 + 小挖占比', '77%', '2024 融资交易结构'],
        ['2025 XCMG 资料销量', formatNumber(compactUnits + largeUnits), `0–10 吨 ${formatNumber(compactUnits)} 台 + 10 吨以上 ${formatNumber(largeUnits)} 台`],
        ['历史型谱覆盖', '75% / 78%', '微小挖 / 中大挖']
      ];

    const narratives = language === 'en'
      ? [
        ['Demand base', 'The market is structurally concentrated in mini and compact machines, but the classes are not interchangeable. 1-4 t products are transport- and access-constrained; 4-10 t products must balance productivity and attachment breadth; medium and large machines are purchased around output, durability and lifecycle support.'],
        ['Competitive reality', 'In 0-10 t, the four leading brands account for 74% of documented volume. Above 10 t, the top three account for 69%. This concentration reflects more than machines: dealer reach, finance, rental relationships, parts availability and resale confidence reinforce the installed base.'],
        ['Product implication', 'XCMG needs two parallel systems. Mini and compact products should learn from Kubota-style application coverage, hydraulic feel and residual value. Medium and large products should be judged against Caterpillar-style productivity, platform depth and lifecycle support.']
      ]
      : [
        ['需求基本盘', '市场销量长期集中在微挖和小挖，但各吨级不能互相替代。1–4 吨首先受运输和进入空间约束；4–10 吨需要平衡效率与属具广度；中大挖则围绕产量、耐久和全生命周期支持进行采购。'],
        ['竞争现实', '0–10 吨市场前四品牌合计占资料销量的 74%，10 吨以上前三品牌合计 69%。这种集中度不仅来自主机，还来自经销覆盖、金融、租赁关系、配件供应和二手机信心对保有量的持续强化。'],
        ['产品含义', 'XCMG 需要并行建设两套能力：微小挖学习久保田式的工况覆盖、液压手感和残值体系；中大挖按照卡特式的生产率、平台深度和生命周期支持进行评价。']
      ];

    setHtml('#overview-summary-content', `
      <div class="kpis overviewKpis expandedKpis">
        ${kpis.map((item, index) => `<div class="kpi${index === 2 ? ' xcmg' : ''}"><span>${esc(item[0])}</span><b>${esc(item[1])}</b><span>${esc(item[2])}</span></div>`).join('')}
      </div>
      <div class="categoryNarrative">
        ${narratives.map((item) => `<article><b>${esc(item[0])}</b><p>${esc(item[1])}</p></article>`).join('')}
      </div>
      <div class="categoryBoundary">
        <strong>${language === 'en' ? 'How to read the page' : '阅读逻辑'}</strong>
        <p>${language === 'en'
          ? 'The page moves from demand to market structure, then to competition, real applications, portfolio coverage and engineering action. A market number describes demand; a specification describes paper capability; only field validation confirms usable performance.'
          : '页面按“需求—市场结构—竞争—真实工况—型谱—工程动作”展开。市场数字说明需求，参数说明纸面能力，只有实机验证才能确认可用性能。'}</p>
      </div>`);
  }

  function renderCycle(data) {
    const values = data.market_cycle;
    const max = Math.max(...values.map((item) => item.units));
    return `
      <article class="cycleChartPanel expandedCyclePanel">
        <div class="chartTitle"><b>${copy.marketCycle}</b><span>${copy.units}</span></div>
        <div class="cycleChart" role="img" aria-label="${copy.marketCycle}">
          ${values.map((item) => `<div class="cycleColumn${item.year === '2023' ? ' peak' : ''}">
            <div class="cycleBar ${item.status.includes('forecast') ? 'forecast' : 'actual'}" style="--height:${(item.units / max * 100).toFixed(1)}%"><span>${formatNumber(item.units)}</span></div>
            <b>${esc(item.year)}</b>
            <small>${item.status.includes('forecast') ? copy.forecast : copy.actual}</small>
          </div>`).join('')}
        </div>
        <div class="chartLegend">
          <span><i class="actual"></i><em>${copy.actual}</em></span>
          <span><i class="forecast"></i><em>${copy.forecast}</em></span>
        </div>
      </article>`;
  }

  function renderMarketDemand(data) {
    const readings = [
      [copy.cycleRead, copy.cycleText],
      [copy.demandDirection, copy.demandText],
      [copy.financeImpact, copy.financeText]
    ];
    const regionHtml = regionalSignals.map((item) => `<article class="regionRow">
      <header><b>${esc(text(item.region))}</b><span>${esc(text(item.states))}</span></header>
      <div><strong>${language === 'en' ? 'Demand pattern' : '需求特征'}</strong><p>${esc(text(item.demand))}</p></div>
      <div><strong>${language === 'en' ? 'Product and validation focus' : '产品与验证重点'}</strong><p>${esc(text(item.response))}</p></div>
    </article>`).join('');
    const customerHtml = customerSegments.map((item) => `<article class="customerRow">
      <h3>${esc(text(item.segment))}</h3>
      <div><b>${language === 'en' ? 'Work profile' : '作业画像'}</b><p>${esc(text(item.work))}</p></div>
      <div><b>${language === 'en' ? 'Purchase logic' : '采购逻辑'}</b><p>${esc(text(item.decision))}</p></div>
      <div><b>${language === 'en' ? 'Product implication' : '产品含义'}</b><p>${esc(text(item.product))}</p></div>
    </article>`).join('');
    const macroHtml = macroSignals.map((item) => `<div class="macroRow">
      <b>${esc(text(item.factor))}</b>
      <p>${esc(text(item.signal))}</p>
      <p>${esc(text(item.impact))}</p>
    </div>`).join('');

    setHtml('#market-demand-content', `
      <div class="cycleLayout expandedCycleLayout">
        ${renderCycle(data)}
        <div class="cycleReading expandedCycleReading">
          ${readings.map((item) => `<div class="readingBlock"><b>${esc(item[0])}</b><p>${esc(item[1])}</p></div>`).join('')}
        </div>
      </div>
      <div class="subsectionHead"><h3>${language === 'en' ? 'Regional demand map' : '区域需求地图'}</h3><p>${language === 'en' ? 'Regional demand changes prototype placement, attachment packages, dealer stock and environmental validation.' : '区域需求直接影响样机投放、属具包、经销库存和环境适应性验证。'}</p></div>
      <div class="regionMatrix">${regionHtml}</div>
      <div class="subsectionHead"><h3>${language === 'en' ? 'Customer segments and buying logic' : '客户结构与购买逻辑'}</h3><p>${language === 'en' ? 'The same nominal machine can require a different package when the customer, operator skill and utilization model change.' : '客户类型、机手水平和利用率模式变化后，同一名义机型需要不同的产品包。'}</p></div>
      <div class="customerMatrix">${customerHtml}</div>
      <div class="subsectionHead"><h3>${language === 'en' ? 'External signals translated into product decisions' : '外部信号如何转化为产品决策'}</h3></div>
      <div class="macroMatrix">
        <div class="macroHeader"><b>${language === 'en' ? 'Factor' : '因素'}</b><b>${language === 'en' ? 'Observed direction' : '观察方向'}</b><b>${language === 'en' ? 'Implication for XCMG' : '对 XCMG 的含义'}</b></div>
        ${macroHtml}
      </div>`);
  }

  function renderMix(data) {
    const series = data.market_mix.series;
    const groups = [
      ['mini', language === 'en' ? 'Mini 0-4 t' : '微挖 0–4 吨'],
      ['compact', language === 'en' ? 'Compact 4-10 t' : '小挖 4–10 吨'],
      ['medium', language === 'en' ? 'Medium 10-33 t' : '中挖 10–33 吨'],
      ['large', language === 'en' ? 'Large above 33 t' : '大挖 33 吨以上']
    ];
    return `
      <article class="mixPanel expandedMixPanel">
        <div class="chartTitle"><b>${copy.mixTitle}</b><span>${copy.mixSubtitle}</span></div>
        <div class="mixRows">
          ${data.market_mix.years.map((year, index) => `<div class="mixRow${year === '2024' ? ' current' : ''}"><b>${year}</b><div class="mixBar">
            ${groups.map(([key]) => `<span class="${key}" style="width:${(series[key][index] * 100).toFixed(1)}%">${Math.round(series[key][index] * 100)}%</span>`).join('')}
          </div></div>`).join('')}
        </div>
        <div class="mixLegend">${groups.map(([key, label]) => `<span><i class="${key}"></i><em>${esc(label)}</em></span>`).join('')}</div>
      </article>`;
  }

  function renderTonnageHeatmap(data) {
    const core = new Set(['1-2 t', '2-3 t', '3-4 t', '4-5 t', '5-6 t', '8-10 t', '12-14 t', '14-16 t', '21-24 t', '24-28 t', '33-40 t', '40-50 t']);
    return `<div class="tonnageHeatmap expandedHeatmap">${data.tonnage_volume.map((item) => {
      const severity = item.yoy <= -0.4 ? 'severe' : item.yoy <= -0.25 ? 'watch' : 'resilient';
      return `<article class="heatCell ${severity}${core.has(item.range) ? ' key' : ''}">
        <span>${esc(item.range)}</span><b>${formatNumber(item.y2024)}</b><small>${(item.yoy * 100).toFixed(1)}%</small>
      </article>`;
    }).join('')}</div>`;
  }

  function renderMarketStructure(data) {
    const groupReadings = language === 'en'
      ? [
        ['Mini 0-4 t', '40%', 'The largest broad class. Access, transport, ground protection, fine control and rental versatility define the product. Core demand sits in 3-4 t, followed by 1-2 t and 2-3 t.'],
        ['Compact 4-10 t', '37%', 'The bridge between small-site access and production. Customers expect wider attachment use, faster travel, stronger digging and more stable lifting without losing transport flexibility.'],
        ['Medium 10-33 t', '16%', 'Utility, foundation and production applications increase the importance of reach, lifting, cycle time, fuel use and cab endurance. Conventional and short-tail pairs carry distinct value.'],
        ['Large above 33 t', '7%', 'Lower volume but high project value. Heavy cycles, loading output, transport preparation, cooling, durability and lifecycle support dominate the purchase decision.']
      ]
      : [
        ['微挖 0–4 吨', '40%', '最大的大类规格。进入空间、运输、地面保护、精细操控和租赁通用性定义产品，核心需求集中在 3–4 吨，其次是 1–2 吨和 2–3 吨。'],
        ['小挖 4–10 吨', '37%', '连接小场地进入能力与生产效率。客户希望获得更广的属具覆盖、更快行走、更强挖掘和更稳定起吊，同时不能失去运输灵活性。'],
        ['中挖 10–33 吨', '16%', '公用工程、基础和产能型施工提高了对工作范围、起吊、循环时间、油耗和全天驾驶舒适性的要求，常规尾与短尾承担不同价值。'],
        ['大挖 33 吨以上', '7%', '销量较低但项目价值高。重载循环、装车产量、运输准备、散热、耐久和生命周期支持主导采购决策。']
      ];
    setHtml('#market-structure-content', `
      <div class="structureLayout expandedStructureLayout">
        ${renderMix(data)}
        <div class="classNarrative">
          ${groupReadings.map((item) => `<article><header><b>${esc(item[0])}</b><strong>${esc(item[1])}</strong></header><p>${esc(item[2])}</p></article>`).join('')}
        </div>
      </div>
      <div class="subsectionHead"><h3>${copy.tonnageMovement}</h3><p>${copy.tonnageExplanation}</p></div>
      ${renderTonnageHeatmap(data)}
      <div class="heatLegend">
        <span><i class="resilient"></i><em>${language === 'en' ? 'Decline under 25%' : '降幅小于 25%'}</em></span>
        <span><i class="watch"></i><em>${language === 'en' ? 'Decline 25-40%' : '降幅 25%–40%'}</em></span>
        <span><i class="severe"></i><em>${language === 'en' ? 'Decline over 40%' : '降幅超过 40%'}</em></span>
        <span><i class="key"></i><em>${language === 'en' ? 'Core historical class' : '历史核心规格'}</em></span>
      </div>
      <div class="structureConclusion">
        <h3>${language === 'en' ? 'What the structure means for portfolio decisions' : '吨级结构对产品组合意味着什么'}</h3>
        <p>${language === 'en'
          ? 'The 2024 correction was not uniform. Some high-volume mini and medium classes contracted sharply, while 4-6 t and 40-50 t were comparatively resilient. The correct response is not to remove every declining class, but to distinguish a cyclical decline from a structural portfolio role. A core class can still require investment when it anchors dealer traffic, rental utilization or an application family.'
          : '2024 年的调整并不均匀：部分高销量微挖和中挖规格降幅较大，而 4–6 吨和 40–50 吨相对更有韧性。产品组合不能简单按“下降就退出”处理，而要区分周期性下滑与结构性角色。即使某核心吨级短期下降，只要它仍承担经销获客、租赁周转或工况族入口，就仍可能需要持续投入。'}</p>
      </div>`);
  }

  function brandPanel(items, title, concentration) {
    const visible = items.filter((item) => ['KUBOTA', 'CAT', 'BOBCAT', 'DEERE', 'TAKEUCHI', 'KOMATSU', 'HITACHI', 'VOLVO', 'LINK-BELT', 'XCMG'].includes(item.brand));
    const max = Math.max(...visible.map((item) => item.units));
    return `<article class="sharePanel expandedSharePanel">
      <header><div><h3>${esc(title)}</h3><span>${copy.sourcePeriod}</span></div><b>${esc(concentration)}</b></header>
      <div class="brandBars">
        ${visible.map((item) => `<div class="${item.brand === 'XCMG' ? 'xcmg' : ''}">
          <span>${esc(item.brand)}</span><i><em style="width:${Math.max(2, item.units / max * 100).toFixed(1)}%"></em></i>
          <b>${esc(item.share_label || `${item.share}%`)}</b><small>${formatNumber(item.units)}</small>
        </div>`).join('')}
      </div>
    </article>`;
  }

  function renderCompetition(data) {
    const tierRows = language === 'en'
      ? [
        ['North American leaders', 'CAT · DEERE', 'Brand trust, broad product platforms, dealer coverage, parts, finance and professional-fleet relationships.'],
        ['Japanese and European specialists', 'KUBOTA · KOMATSU · VOLVO · TAKEUCHI', 'Deep application expertise, hydraulic maturity, fuel efficiency, compact packaging and strong class-specific reputations.'],
        ['Full-line and value challengers', 'SANY · XCMG · LIUGONG · DEVELON · HYUNDAI', 'Competitive acquisition cost and improving portfolios; must close support, residual-value and verified field-performance gaps.'],
        ['Niche and long-tail brands', 'Regional / specialist brands', 'Win through a narrow application, channel or price position, but lack the scale and coverage of the leading systems.']
      ]
      : [
        ['北美本土主导品牌', 'CAT · DEERE', '品牌信任、宽型谱平台、经销覆盖、配件、金融和专业车队关系共同构成优势。'],
        ['日欧专业品牌', 'KUBOTA · KOMATSU · VOLVO · TAKEUCHI', '在特定吨级和工况形成深厚能力，液压成熟、油耗低、包络紧凑且客户认知清晰。'],
        ['全产品线与价值挑战者', 'SANY · XCMG · LIUGONG · DEVELON · HYUNDAI', '采购成本有竞争力、型谱持续完善，但仍需补齐服务、残值和经验证的实机表现。'],
        ['区域与细分品牌', '区域品牌 / 专业品牌', '依靠窄工况、渠道或价格切入，但缺少领先体系的规模和覆盖。']
      ];
    const benchmarkTable = benchmarkRows.map((row) => `<div class="benchmarkCompareRow">
      <b>${esc(text(row.dimension))}</b>
      <p>${esc(text(row.kubota))}</p>
      <p>${esc(text(row.xcmgMini))}</p>
      <p>${esc(text(row.cat))}</p>
      <p>${esc(text(row.xcmgLarge))}</p>
    </div>`).join('');

    setHtml('#competition-content', `
      <div class="competitionGrid expandedCompetitionGrid">
        ${brandPanel(data.competition_2025.compact, copy.competitionCompact, copy.compactConcentration)}
        ${brandPanel(data.competition_2025.mid_large, copy.competitionLarge, copy.largeConcentration)}
      </div>
      <div class="competitionReading">
        <article><b>${language === 'en' ? 'Mini and compact market' : '微小挖市场'}</b><p>${language === 'en' ? 'Kubota, CAT, Bobcat and Deere together account for roughly three quarters of the documented market. Their strength is reinforced by compact-equipment ecosystems, dealer familiarity, attachment breadth and rental penetration. XCMG must compete against that complete ownership path, not only against a specification sheet.' : '久保田、卡特、山猫和迪尔合计约占资料市场的四分之三。其优势由小型设备生态、经销熟悉度、属具广度和租赁渗透共同强化。XCMG 面对的是完整的拥有与使用路径，而不只是参数表。'}</p></article>
        <article><b>${language === 'en' ? 'Medium and large market' : '中大挖市场'}</b><p>${language === 'en' ? 'CAT, Komatsu and Deere dominate through professional-fleet trust, productivity, reliability and lifecycle support. The purchase decision extends from the machine to finance, service, parts, buyback and remanufacturing. A lower purchase price only matters when output and uptime are credible.' : '卡特、小松和迪尔依靠专业车队信任、生产率、可靠性和生命周期支持占据主导。采购判断从主机延伸到金融、服务、配件、回购和再制造；只有产量与开工率可信时，更低采购价才有意义。'}</p></article>
      </div>
      <div class="subsectionHead"><h3>${language === 'en' ? 'Competitive tiers' : '竞争梯队'}</h3><p>${language === 'en' ? 'Each tier wins through a different combination of product, channel and ownership economics.' : '不同梯队依靠不同的产品、渠道与拥有成本组合取胜。'}</p></div>
      <div class="brandTierTable expandedTierTable">
        <div class="tierHeader"><b>${language === 'en' ? 'Tier' : '梯队'}</b><b>${language === 'en' ? 'Representative brands' : '代表品牌'}</b><b>${language === 'en' ? 'System advantage' : '体系优势'}</b></div>
        ${tierRows.map((row) => `<div><strong>${esc(row[0])}</strong><span>${esc(row[1])}</span><p>${esc(row[2])}</p></div>`).join('')}
      </div>
      <div class="subsectionHead"><h3>${language === 'en' ? 'Two benchmark systems, not one universal benchmark' : '两套标杆体系，而不是一个万能标杆'}</h3><p>${language === 'en' ? 'Kubota represents the compact-equipment ownership path; Caterpillar represents the professional-fleet lifecycle system.' : '久保田代表微小挖的使用与拥有路径，卡特代表中大挖的专业车队生命周期体系。'}</p></div>
      <div class="benchmarkCompareTable">
        <div class="benchmarkCompareHeader">
          <b>${language === 'en' ? 'Dimension' : '维度'}</b>
          <b>KUBOTA</b><b>XCMG 0–10 t</b><b>CATERPILLAR</b><b>XCMG &gt;10 t</b>
        </div>
        ${benchmarkTable}
      </div>`);
  }

  function renderApplications() {
    const gallery = scenarios.map((item, index) => `<figure class="applicationFigure${index === 0 || index === 5 ? ' wide' : ''}">
      <img src="${esc(item.image)}" alt="${esc(text(item.title))}">
      <figcaption>
        <span>${esc(item.className)}</span>
        <h3>${esc(text(item.title))}</h3>
        <b>${esc(text(item.customer))}</b>
        <p>${esc(text(item.narrative))}</p>
      </figcaption>
    </figure>`).join('');
    const matrixHeader = language === 'en'
      ? ['Application', 'Packaging', 'Range', 'Hydraulics', 'Attachments', 'Stability', 'Visibility', 'Service']
      : ['典型工况', '整机包络', '工作范围', '液压', '属具', '稳定性', '视野', '维修'];
    const matrix = capabilityMatrix.map((row) => `<div class="capabilityRow"><b>${esc(text(row.scenario))}</b>${['packaging', 'range', 'hydraulics', 'attachments', 'stability', 'visibility', 'service'].map((key) => `<span class="${row[key] === '●' ? 'critical' : 'supporting'}">${row[key]}</span>`).join('')}</div>`).join('');
    setHtml('#applications-content', `
      <div class="applicationGallery">${gallery}</div>
      <div class="applicationAnalysis">
        <article><h3>${language === 'en' ? 'Why application evidence changes the benchmark' : '为什么工况证据会改变对标结论'}</h3><p>${language === 'en' ? 'A machine can look competitive in a static specification table and still lose the customer task. Transport mass may eliminate an otherwise strong mini excavator; a short stick can limit trench work; swing braking can reduce precision; low auxiliary flow can narrow attachment coverage; poor access can turn a minor service event into a day of downtime. The benchmark therefore has to follow the full task chain from transport and setup through work, repositioning, attachment change and maintenance.' : '一台设备可能在静态参数表中很强，却仍然输掉客户任务：运输质量可能直接淘汰一台纸面优秀的微挖；斗杆过短会限制沟槽；回转制动影响精度；AUX 流量不足压缩属具覆盖；维修可达性差会把小故障变成整天停机。因此，对标必须沿着运输、进场、作业、转场、换属具和维护的完整任务链展开。'}</p></article>
        <article><h3>${language === 'en' ? 'How to convert a scene into an engineering target' : '如何把场景转化为工程目标'}</h3><p>${language === 'en' ? 'Start with the physical boundary of the job: access width, trailer combination, trench depth, lift load, truck height, slope and ground condition. Then define the machine package and measure cycle time, controllability, fuel or energy use, stability, visibility and service time. Only after this chain is complete should a feature be called an advantage.' : '先确定任务的物理边界：通道宽度、拖车组合、沟槽深度、吊装重量、装车高度、坡度和地面条件；再定义整机配置并测量循环时间、操控性、油耗或能耗、稳定性、视野和维护时间。只有完成这条链路后，一个配置才能被称为优势。'}</p></article>
      </div>
      <div class="subsectionHead"><h3>${copy.fieldMatrix}</h3><p>${language === 'en' ? 'Solid dots indicate a primary design constraint; open dots indicate an important supporting factor.' : '实心点表示主要设计约束，空心点表示重要支持因素。'}</p></div>
      <div class="capabilityMatrix">
        <div class="capabilityHeader">${matrixHeader.map((item) => `<b>${esc(item)}</b>`).join('')}</div>
        ${matrix}
      </div>`);
  }

  function statusLabel(status) {
    const labels = {
      covered: {zh: '已覆盖', en: 'Covered'},
      partial: {zh: '部分覆盖', en: 'Partial'},
      pilot_in_source: {zh: '历史先导', en: 'Historical pilot'},
      covered_overlap: {zh: '型谱重叠', en: 'Overlap'},
      gap: {zh: '结构空白', en: 'Gap'},
      gap_low_priority: {zh: '低优先级空白', en: 'Low-priority gap'}
    };
    return text(labels[status] || {zh: status, en: status});
  }

  function historicalDirectionLabel(direction) {
    if (language === 'en') return direction;
    const labels = {
      'no introduction recommended': '暂不建议导入',
      'higher-power variant': '补充高功率版本',
      'cab and PRO package': '补充驾驶室与 PRO 配置包',
      'lightweight conventional-tail complement': '补充轻量化常规尾机型',
      'validate sales readiness': '复核量产与销售准备度',
      'power and travel upgrade': '升级动力与行走性能',
      'generation update and short-tail complement': '代际升级并补充短尾机型',
      'height, mass and stability optimization': '优化高度、质量与稳定性',
      'maintain class coverage': '保持该吨级覆盖',
      'simplify overlap and strengthen short-tail': '精简重叠机型并强化短尾方案',
      'historical XE170U proposal': '历史 XE170U 产品方案',
      'no introduction recommended in source': '历史判断为暂不导入',
      'conventional and short-tail pair': '形成常规尾与短尾组合',
      'strength and control optimization': '强化结构与操控',
      'long-reach complement': '补充加长臂方案',
      'short-tail and heavy-duty complements': '补充短尾与重载方案',
      'transport and loading upgrade': '升级运输与装车工况方案'
    };
    return labels[direction] || direction;
  }

  function renderPortfolioBand(title, benchmark, items) {
    return `<article class="portfolioBand expandedPortfolioBand">
      <header><div><h3>${esc(title)}</h3><span>${esc(benchmark)}</span></div></header>
      <div class="portfolioRows">
        ${items.map((item) => `<div class="portfolioRow ${esc(item.status)}">
          <b>${esc(item.range)}</b><strong>${esc(item.xcmg)}</strong><span>${esc(statusLabel(item.status))}</span><p>${esc(historicalDirectionLabel(item.historical_direction))}</p>
        </div>`).join('')}
      </div>
    </article>`;
  }

  function renderPortfolio(data) {
    const portfolioGallery = officialPortfolio.map((item) => `<figure class="portfolioMachine">
      <img src="${esc(item.image)}" alt="${esc(item.model)}">
      <figcaption><span>${esc(item.range)}</span><b>${esc(item.model)}</b><small>${esc(text(item.role))}</small></figcaption>
    </figure>`).join('');
    const compactTitle = language === 'en' ? 'Mini and compact portfolio, 0-10 t' : '微小挖型谱，0–10 吨';
    const largeTitle = language === 'en' ? 'Medium and large portfolio, above 10 t' : '中大挖型谱，10 吨以上';
    setHtml('#portfolio-content', `
      <div class="portfolioGallery">${portfolioGallery}</div>
      <div class="portfolioReading">
        <article><b>${language === 'en' ? 'Mini and compact benchmark: Kubota' : '微小挖标杆：久保田'}</b><p>${language === 'en' ? 'The benchmark is not one Kubota model. It is the ability to cover short-tail and conventional-tail needs, provide appropriate trim levels, tune hydraulics for fine combined motion and preserve reliability and resale confidence through the ownership cycle.' : '标杆不是某一款久保田机型，而是同时覆盖短尾与常规尾、提供合适高低配、把液压调校到细腻复合动作，并在整个拥有周期中维持可靠性与残值信心的能力。'}</p></article>
        <article><b>${language === 'en' ? 'Medium and large benchmark: Caterpillar' : '中大挖标杆：卡特彼勒'}</b><p>${language === 'en' ? 'The benchmark extends from electrohydraulic control and application packages to dealer service, finance, parts, buyback and remanufacturing. XCMG must translate acquisition-cost advantage into verified output and lifecycle value.' : '标杆从电液控制和工况包延伸到经销服务、金融、配件、回购和再制造。XCMG 需要把采购成本优势转化为经过验证的产量和生命周期价值。'}</p></article>
      </div>
      <div class="portfolioCoverageSummary">
        <div><span>${language === 'en' ? 'Historical mini/compact coverage' : '历史微小挖覆盖'}</span><b>${Math.round(data.portfolio.historical_coverage.mini_compact * 100)}%</b><p>${language === 'en' ? 'Coverage by nominal class did not fully close tail configuration, trim and application gaps.' : '名义吨级覆盖并未完全解决尾部形式、高低配和工况空白。'}</p></div>
        <div><span>${language === 'en' ? 'Historical medium/large coverage' : '历史中大挖覆盖'}</span><b>${Math.round(data.portfolio.historical_coverage.mid_large * 100)}%</b><p>${language === 'en' ? 'Short-tail, heavy-duty, long-reach and transport combinations remained incomplete.' : '短尾、重载、加长臂和运输组合仍不完整。'}</p></div>
        <div><span>${language === 'en' ? 'Coverage rule' : '覆盖判断'}</span><b>${language === 'en' ? 'Task fit' : '任务适配'}</b><p>${language === 'en' ? 'One model in a class is not complete coverage unless it meets the major task families.' : '同吨级有一款机型不等于完整覆盖，必须满足主要任务族。'}</p></div>
      </div>
      <div class="subsectionHead"><h3>${copy.portfolioMatrix}</h3><p>${language === 'en' ? 'Status reflects the historical portfolio view and requires current sales-readiness confirmation.' : '状态反映历史型谱判断，当前可售状态仍需复核。'}</p></div>
      <div class="portfolioMatrixGrid">
        ${renderPortfolioBand(compactTitle, language === 'en' ? 'KUBOTA benchmark' : '久保田标杆', data.portfolio.mini_compact)}
        ${renderPortfolioBand(largeTitle, language === 'en' ? 'CATERPILLAR benchmark' : '卡特彼勒标杆', data.portfolio.mid_large)}
      </div>
      <div class="portfolioConclusion">
        <h3>${language === 'en' ? 'Portfolio decisions that follow from the gaps' : '由型谱空白推导出的产品决策'}</h3>
        <p>${language === 'en'
          ? 'The priority is not maximum model count. It is a coherent product family: high-volume mini classes need transport-appropriate short-tail and conventional-tail choices; 4-10 t products need attachment and productivity packages; medium classes need conventional/short-tail pairs and long-stick options; large machines need transport, heavy-duty, loading and lifting packages. Shared controls, service interfaces, telematics and attachment standards should reduce complexity across the line.'
          : '重点不是追求最大机型数量，而是形成连贯的产品族：高销量微挖需要符合运输边界的短尾/常规尾选择；4–10 吨需要属具与效率配置包；中挖需要常规尾/短尾组合和长斗杆选项；大挖需要运输、重载、装车和起吊配置包。控制逻辑、维修接口、远程管理和属具标准应跨产品统一，以降低复杂度。'}</p>
      </div>`);
  }

  function renderIssueHeatmap(data) {
    const themes = Object.keys(issueThemeLabels);
    const models = data.improvement_ledger.models;
    const header = `<div class="issueHeatHeader"><b>${language === 'en' ? 'Model' : '机型'}</b>${themes.map((theme) => `<b>${esc(text(issueThemeLabels[theme]))}</b>`).join('')}<b>${language === 'en' ? 'Items' : '条目'}</b></div>`;
    const rows = models.map((model) => `<div class="issueHeatRow"><strong>${esc(model.model)}</strong>${themes.map((theme) => `<span class="${model.themes.includes(theme) ? 'active' : ''}" title="${esc(text(issueThemeLabels[theme]))}">${model.themes.includes(theme) ? '●' : '·'}</span>`).join('')}<b>${model.issue_count}</b></div>`).join('');
    return `<div class="issueHeatmap">${header}${rows}</div>`;
  }

  function renderTargets(data) {
    const totals = data.historical_sales_plan.totals;
    const max = Math.max(...totals.map((item) => item.units));
    const modelMax = Math.max(...data.historical_sales_plan.top_2027_models.map((item) => item.units));
    return `<div class="targetLayout expandedTargetLayout">
      <article class="targetChart overviewPanel">
        <div class="chartTitle"><b>${copy.targetTitle}</b><span>${copy.targetNote}</span></div>
        <div class="targetColumns">
          ${totals.map((item) => `<div><i class="${item.type.includes('actual') ? 'actual' : 'planned'}" style="height:${(item.units / max * 100).toFixed(1)}%"><span>${formatNumber(item.units)}</span></i><b>${item.year}</b><small>${item.type.includes('actual') ? copy.actual : copy.plan} ${item.share}%</small></div>`).join('')}
        </div>
      </article>
      <article class="modelTarget overviewPanel">
        <div class="chartTitle"><b>${language === 'en' ? 'Largest model contributions in the historical 2027 target' : '历史 2027 目标中的主要型号贡献'}</b><span>${copy.units}</span></div>
        <div class="modelTargetBars">
          ${data.historical_sales_plan.top_2027_models.map((item) => `<div><span>${esc(item.model)}</span><i><em style="width:${(item.units / modelMax * 100).toFixed(1)}%"></em></i><b>${formatNumber(item.units)}</b></div>`).join('')}
        </div>
        <p>${language === 'en' ? 'The historical path concentrated most growth in 3-6 t products. Current planning should replace targets with actual orders, retail deliveries, dealer inventory, repeat purchase and field-support capacity.' : '历史路径把大部分增量集中在 3–6 吨产品。当前规划需要用实际订单、终端交付、经销库存、复购与现场支持能力更新这些目标。'}</p>
      </article>
    </div>`;
  }

  function renderActions(data) {
    const themes = Object.keys(issueThemeLabels);
    const themeCounts = Object.fromEntries(themes.map((theme) => [theme, data.improvement_ledger.models.filter((model) => model.themes.includes(theme)).length]));
    const maxTheme = Math.max(...Object.values(themeCounts));
    const themeNarratives = {
      transport: {zh: '整机质量、运输高度、履带宽度、可拆配重和拖车余量必须按整备状态计算。', en: 'Operating mass, transport height, shoe width, removable counterweight and trailer margin must be calculated in equipped condition.'},
      travel: {zh: '行走速度、脚踏死区、直线性、启停晃动与自动双速共同影响转场效率。', en: 'Travel speed, pedal deadband, straight-line behavior, start/stop motion and auto two-speed jointly affect repositioning.'},
      work_equipment: {zh: '斗杆、斗容、挖掘力、起吊与工作范围要按具体任务定义，而不是只追求单项峰值。', en: 'Stick, bucket, digging force, lifting and working range must be defined by task rather than one peak value.'},
      hydraulics: {zh: '主泵、AUX 流量、属具管路、快换和阀控标定决定多属具覆盖与复合动作。', en: 'Main pump, auxiliary flow, attachment lines, coupler and valve calibration determine attachment coverage and combined motion.'},
      swing_control: {zh: '回转力矩、制动线性和回摆会直接影响装车循环与精细作业。', en: 'Swing torque, braking linearity and rebound directly affect loading cycles and precision work.'},
      stability: {zh: '底盘、配重、履带和重心决定坡地、起吊和重载工况的安全边界。', en: 'Undercarriage, counterweight, tracks and center of gravity define the safety envelope for slopes, lifting and heavy duty.'},
      cab_hmi: {zh: '座椅、脚踏、扶手、门、显示器、英制单位和控制布局影响全天作业与误操作风险。', en: 'Seat, pedals, armrests, door, display, imperial units and control layout affect all-day work and misuse risk.'},
      vision: {zh: '后视与全景影像、照明和报警是城市、起吊、倒车和人员附近作业的基础。', en: 'Rear/surround cameras, lighting and alarms are foundational around traffic, lifting, reversing and personnel.'},
      service: {zh: '加注口、可达性、防腐、资料和备件响应决定停机时间和残值。', en: 'Fill points, access, corrosion protection, documentation and parts response determine downtime and residual value.'}
    };
    const themesHtml = themes.map((theme) => `<article class="themeRow">
      <div><b>${esc(text(issueThemeLabels[theme]))}</b><span>${themeCounts[theme]} ${language === 'en' ? 'models' : '个机型'}</span></div>
      <i><em style="width:${(themeCounts[theme] / maxTheme * 100).toFixed(1)}%"></em></i>
      <p>${esc(text(themeNarratives[theme]))}</p>
    </article>`).join('');
    const ledgerRows = detailedLedger.map((item) => `<div class="ledgerRow">
      <b>${esc(item.model)}</b>
      <p data-label="${language === 'en' ? 'Documented gap' : '具体差距'}">${esc(text(item.gaps))}</p>
      <p data-label="${language === 'en' ? 'Engineering direction' : '工程方向'}">${esc(text(item.action))}</p>
      <p data-label="${language === 'en' ? 'Required validation' : '验证要求'}">${esc(text(item.validation))}</p>
    </div>`).join('');
    const dataBasisRows = language === 'en'
      ? [
        ['AEM', 'Industry cycle and tonnage volume', 'Retain historical actuals; replace old forecasts before current decisions.'],
        ['EDA', 'Financed-transaction mix and brand structure', 'Use units and shares for the stated period; do not infer current rank without refresh.'],
        ['Customer and channel evidence', 'Applications, purchase logic and unmet needs', 'Use to define test conditions; do not replace controlled engineering tests.'],
        ['Engineering and service evidence', 'Product gaps, serviceability and validation targets', 'Close only with current production, prototype or field-test evidence.']
      ]
      : [
        ['AEM', '行业周期与吨级销量', '保留历史实际值；当前决策前用最新实际值替换旧预测。'],
        ['EDA', '融资交易结构与品牌格局', '按标注时间段使用销量和份额；未经更新不推导当前排名。'],
        ['客户与渠道证据', '工况、采购逻辑与未满足需求', '用于定义试验条件，不能替代受控工程试验。'],
        ['工程与服务证据', '产品差距、维修性与验证目标', '只有当前量产、样机或实机试验证据才能关闭问题。']
      ];
    setHtml('#actions-content', `
      <div class="themeRows">${themesHtml}</div>
      <div class="subsectionHead"><h3>${copy.issueMap}</h3><p>${copy.issueCount}</p></div>
      ${renderIssueHeatmap(data)}
      <div class="subsectionHead"><h3>${copy.ledgerTitle}</h3><p>${language === 'en' ? 'The table converts repeated observations into a measurable validation agenda; it does not claim that historical actions are complete.' : '表格把重复出现的问题转化为可测量的验证任务，不代表历史动作已经完成。'}</p></div>
      <div class="detailedLedger">
        <div class="ledgerHeader"><b>${language === 'en' ? 'Model' : '机型'}</b><b>${language === 'en' ? 'Documented gap' : '具体差距'}</b><b>${language === 'en' ? 'Engineering direction' : '工程方向'}</b><b>${language === 'en' ? 'Required validation' : '验证要求'}</b></div>
        ${ledgerRows}
      </div>
      <div class="subsectionHead"><h3>${language === 'en' ? 'Historical portfolio and sales path' : '历史型谱与销量路径'}</h3><p>${copy.targetNote}</p></div>
      ${renderTargets(data)}
      <div class="validationFramework">
        <h3>${language === 'en' ? 'A practical closure standard' : '可执行的差距关闭标准'}</h3>
        <div>
          <article><span>01</span><b>${language === 'en' ? 'Configuration confirmed' : '配置确认'}</b><p>${language === 'en' ? 'Confirm current production content, optional boundaries, equipped mass and regional variants.' : '确认当前量产内容、选配边界、整备质量和区域版本。'}</p></article>
          <article><span>02</span><b>${language === 'en' ? 'Controlled comparison' : '受控对比'}</b><p>${language === 'en' ? 'Use the same site, operator, attachment, material and duty cycle against the benchmark.' : '使用同场地、同机手、同属具、同物料和同循环与标杆对比。'}</p></article>
          <article><span>03</span><b>${language === 'en' ? 'Field confirmation' : '现场确认'}</b><p>${language === 'en' ? 'Run with North American customers and record productivity, fuel, operator feedback and service events.' : '由北美客户实际使用并记录效率、油耗、机手反馈和维修事件。'}</p></article>
          <article><span>04</span><b>${language === 'en' ? 'Release evidence' : '发布证据'}</b><p>${language === 'en' ? 'Close the item only after the validated solution is reflected in production, manuals, parts and sales configuration.' : '验证方案进入量产、手册、备件和销售配置后才关闭条目。'}</p></article>
        </div>
      </div>
      <div class="subsectionHead"><h3>${copy.dataBasis}</h3><p>${copy.dataBasisText}</p></div>
      <div class="dataBasisTable">
        <div class="dataBasisHeader"><b>${language === 'en' ? 'Evidence system' : '证据体系'}</b><b>${language === 'en' ? 'Primary use' : '主要用途'}</b><b>${language === 'en' ? 'Current-use rule' : '当前使用规则'}</b></div>
        ${dataBasisRows.map((row) => `<div><b>${esc(row[0])}</b><p>${esc(row[1])}</p><p>${esc(row[2])}</p></div>`).join('')}
      </div>`);
  }

  function setEnglishShell() {
    if (language !== 'en') return;
    document.documentElement.lang = locale;
    document.title = 'North American Excavator Market and Product Insight | XCMG ARC';
  }

  async function init() {
    setEnglishShell();
    try {
      const response = await fetch('data/ppt-insights/excavator-market-overview.json', {cache: 'no-store'});
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      renderSummary(data);
      renderMarketDemand(data);
      renderMarketStructure(data);
      renderCompetition(data);
      renderApplications();
      renderPortfolio(data);
      renderActions(data);
      document.body.dataset.overviewReady = 'true';
      window.dispatchEvent(new Event('resize'));
    } catch (error) {
      console.error(error);
      const message = language === 'en'
        ? 'The analysis data could not be loaded. Open the stable local preview address and refresh once.'
        : '分析数据未能载入，请使用稳定的本地预览地址并刷新一次。';
      setHtml('#overview-summary-content', `<div class="scopeBoundary">${esc(message)}</div>`);
      document.body.dataset.overviewReady = 'error';
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, {once: true});
  } else {
    init();
  }
})();
