# 微博信息采集
## 采集需求
我们的任务要求采集大V列表，并且给定一个微博大V，要求采集ta所拥有粉丝的列表以及他们指定时间段内的所有微博。
## 数据格式
采集得到的数据要求为 json 格式，要求的字段及描述如下：

  // user
  [
    {
      user_id: "",    // 用户的 ID
      nick_name: "",  // 昵称
      province: "",   // 所在省
      city: "",       // 所在市
      intro: "",      // 个人简介
      birthday: "",   // 生日
      gender: "",     // 性别
      weibo_num: 0,   // 微博发表数
      fans: [
        // 粉丝用户 id 列表
      ],
      followers: [
        // 关注用户 id 列表
      ]
    },
    ...
  ]
  // weibo
  [
    {
      weibo_url: "",        // 这条微博的 URL
      user_id: "",          // 这则微博作者的ID
      content: "",          // 微博的内容
      image_group: [],      // 微博附带图的URL
      tool: "",             // 发布的工具
      created_at: "",       // 微博发表时间
      repost_num: 0,        // 转发数
      comment_num: 0,       // 评论数
      like_num: 0,          // 点赞数
      repost_weibo_url: ""  // 如果是转发，源微博的 URL
    },
    ...
  ]
  
## 评分标准
- 采集到500个大V及其关注者列表（user 表）：1分
- 采集到这些关注者最近1小时内的全部微博（weibo 表）：2分
- 编写或利用现有的爬虫框架进行多线程采集和持续更新：3分
