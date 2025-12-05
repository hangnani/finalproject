<template>
  <div class="settings-container">
    <div class="page-header">
      <h2>设置</h2>
    </div>
    
    <el-tabs v-model="activeTab" class="settings-tabs">
      <!-- 通知设置 -->
      <el-tab-pane label="通知设置" name="notifications">
        <el-card shadow="hover" class="setting-card">
          <h3 class="setting-title">通知偏好</h3>
          <el-form :model="notificationSettings" label-position="top" class="settings-form">
            <!-- 课程提醒 -->
            <el-form-item label="课程提醒">
              <el-switch v-model="notificationSettings.courseReminders" active-text="开启" inactive-text="关闭" @change="saveSettings"></el-switch>
              <div class="setting-description">课程开始前15分钟提醒</div>
            </el-form-item>
            
            <!-- 外卖订单状态通知 -->
            <el-form-item label="外卖订单通知">
              <el-switch v-model="notificationSettings.orderNotifications" active-text="开启" inactive-text="关闭" @change="saveSettings"></el-switch>
              <div class="setting-description">订单状态更新时通知</div>
            </el-form-item>
            
            <!-- 二手交易消息 -->
            <el-form-item label="二手交易消息">
              <el-switch v-model="notificationSettings.secondhandMessages" active-text="开启" inactive-text="关闭" @change="saveSettings"></el-switch>
              <div class="setting-description">收到新消息时通知</div>
            </el-form-item>
            
            <!-- 积分变动通知 -->
            <el-form-item label="积分变动通知">
              <el-switch v-model="notificationSettings.pointNotifications" active-text="开启" inactive-text="关闭" @change="saveSettings"></el-switch>
              <div class="setting-description">积分变动时通知</div>
            </el-form-item>
          </el-form>
        </el-card>
        
        <el-card shadow="hover" class="setting-card mt-20">
          <h3 class="setting-title">点餐提醒设置</h3>
          <el-form :model="orderReminderSettings" label-position="top" class="settings-form">
            <!-- 上课中提醒点餐 -->
            <el-form-item label="上课中提醒点餐">
              <el-switch v-model="orderReminderSettings.classReminders" active-text="开启" inactive-text="关闭" @change="saveSettings"></el-switch>
              <div class="setting-description">课程结束前1小时提醒点餐</div>
            </el-form-item>
            
            <!-- 没课时提醒点餐 -->
            <el-form-item label="没课时提醒点餐">
              <el-switch v-model="orderReminderSettings.freeTimeReminders" active-text="开启" inactive-text="关闭" @change="saveSettings"></el-switch>
              <div class="setting-description">饭点时间提醒点餐</div>
            </el-form-item>
            
            <!-- 提醒时间设置 -->
            <el-form-item label="提醒时间" v-if="orderReminderSettings.freeTimeReminders">
              <el-time-picker
                v-model="orderReminderSettings.reminderTimes"
                range
                placeholder="选择提醒时间范围"
                @change="saveSettings"
                class="time-picker"
              ></el-time-picker>
              <div class="setting-description">没课时的提醒时间段</div>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>
      
      <!-- 饮食偏好 -->
      <el-tab-pane label="饮食偏好" name="diet">
        <el-card shadow="hover" class="setting-card">
          <h3 class="setting-title">饮食禁忌</h3>
          <el-form :model="dietSettings" label-position="top" class="settings-form">
            <el-form-item label="忌口食材">
              <el-select
                v-model="dietSettings.tabooIngredients"
                multiple
                filterable
                allow-create
                default-first-option
                placeholder="选择或输入忌口食材"
                @change="saveSettings"
                class="select-input"
              >
                <el-option label="辣椒" value="辣椒"></el-option>
                <el-option label="香菜" value="香菜"></el-option>
                <el-option label="葱" value="葱"></el-option>
                <el-option label="姜" value="姜"></el-option>
                <el-option label="蒜" value="蒜"></el-option>
                <el-option label="海鲜" value="海鲜"></el-option>
                <el-option label="牛肉" value="牛肉"></el-option>
                <el-option label="羊肉" value="羊肉"></el-option>
              </el-select>
              <div class="setting-description">选择您的忌口食材，系统将在推荐时避开</div>
            </el-form-item>
            
            <!-- 饮食类型偏好 -->
            <el-form-item label="饮食类型偏好">
              <el-checkbox-group v-model="dietSettings.preferredTypes" @change="saveSettings">
                <el-checkbox label="素食"></el-checkbox>
                <el-checkbox label="肉食"></el-checkbox>
                <el-checkbox label="清淡"></el-checkbox>
                <el-checkbox label="重口味"></el-checkbox>
                <el-checkbox label="健康餐"></el-checkbox>
                <el-checkbox label="快餐"></el-checkbox>
              </el-checkbox-group>
              <div class="setting-description">选择您偏好的饮食类型</div>
            </el-form-item>
            
            <!-- 价格偏好 -->
            <el-form-item label="价格偏好">
              <el-slider
                v-model="dietSettings.pricePreference"
                :min="1"
                :max="5"
                :marks="{ 1: '实惠', 2: '', 3: '适中', 4: '', 5: '高端' }"
                @change="saveSettings"
              ></el-slider>
              <div class="setting-description">选择您的价格偏好，影响推荐排序</div>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>
      
      <!-- 积分设置 -->
      <el-tab-pane label="积分设置" name="points">
        <el-card shadow="hover" class="setting-card">
          <h3 class="setting-title">积分说明</h3>
          <div class="points-info">
            <p>• 点外卖：每消费1元获得1积分</p>
            <p>• 发布二手商品：发布成功获得5积分，成交后获得20积分</p>
            <p>• 购买二手商品：每消费1元获得1积分</p>
            <p>• 邀请好友：成功邀请获得50积分</p>
          </div>
          
          <h3 class="setting-title mt-20">积分兑换</h3>
          <div class="rewards-list">
            <el-card v-for="reward in rewards" :key="reward.id" class="reward-card" shadow="hover">
              <div class="reward-content">
                <div class="reward-info">
                  <h4>{{ reward.name }}</h4>
                  <p>{{ reward.description }}</p>
                </div>
                <div class="reward-action">
                  <span class="point-cost">{{ reward.points }}积分</span>
                  <el-button type="primary" @click="exchangeReward(reward)" :disabled="userPoints < reward.points">
                    {{ userPoints < reward.points ? '积分不足' : '立即兑换' }}
                  </el-button>
                </div>
              </div>
            </el-card>
          </div>
        </el-card>
      </el-tab-pane>
      
      <!-- 关于 -->
      <el-tab-pane label="关于" name="about">
        <el-card shadow="hover" class="setting-card">
          <div class="about-content">
            <h3>智能校园生活助手</h3>
            <p>版本：1.0.0</p>
            <p>开发者：校园生活助手团队</p>
            <p>描述：为校园师生提供便捷的校园生活服务</p>
            <p>功能：二手交易、课程表管理、校园点餐、积分系统</p>
          </div>
        </el-card>
      </el-tab-pane>
      
      <!-- 调试设置 -->
      <el-tab-pane label="调试设置" name="debug">
        <el-card shadow="hover" class="setting-card">
          <h3 class="setting-title">点餐提醒调试</h3>
          <div class="debug-content">
            <el-form label-position="top" class="settings-form">
              <!-- 模拟当前时间 -->
              <el-form-item label="模拟时间">
                <el-time-picker
                  v-model="debugTime"
                  format="HH:mm"
                  placeholder="选择要模拟的时间"
                  class="time-picker"
                ></el-time-picker>
                <div class="setting-description">设置模拟时间来测试点餐提醒功能</div>
              </el-form-item>
              
              <!-- 调试操作按钮 -->
              <el-form-item label="调试操作">
                <div class="debug-buttons">
                  <el-button type="primary" @click="testReminderNow">立即触发提醒</el-button>
                  <el-button @click="setDebugTime">应用模拟时间</el-button>
                  <el-button type="danger" @click="resetDebugTime">重置为当前时间</el-button>
                </div>
              </el-form-item>
              
              <!-- 调试信息 -->
              <el-form-item label="调试信息">
                <div class="debug-info">
                  <p>• 当前实际时间：{{ currentRealTime }}</p>
                  <p>• 模拟时间：{{ debugTime ? debugTime : '未设置' }}</p>
                  <p>• 下一次提醒时间：{{ nextReminderTime }}</p>
                </div>
              </el-form-item>
            </el-form>
          </div>
        </el-card>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'

export default {
  name: 'Settings',
  computed: {
    ...mapState(['settings', 'userPoints']),
    ...mapGetters(['notificationSettings', 'orderReminderSettings', 'dietSettings'])
  },
  data() {
    return {
      activeTab: 'notifications',
      // 积分相关
      rewards: [
        {
          id: 1,
          name: '外卖5元优惠券',
          description: '满20元可用',
          points: 500
        },
        {
          id: 2,
          name: '二手交易免手续费',
          description: '单次使用，免除交易手续费',
          points: 300
        },
        {
          id: 3,
          name: '外卖8折优惠券',
          description: '无门槛使用',
          points: 800
        },
        {
          id: 4,
          name: 'VIP标识',
          description: '个人主页显示VIP标识，有效期1个月',
          points: 1200
        }
      ],
      // 调试相关数据
      debugTime: null,
      currentRealTime: '',
      nextReminderTime: '11:00, 17:00',
      realTimeInterval: null
    }
  },
  // 生命周期钩子
  created() {
    this.updateCurrentRealTime()
    // 每秒更新一次实际时间
    this.realTimeInterval = setInterval(() => {
      this.updateCurrentRealTime()
    }, 1000)
  },
  
  beforeDestroy() {
    // 清除定时器
    if (this.realTimeInterval) {
      clearInterval(this.realTimeInterval)
    }
  },
  
  methods: {
    ...mapActions(['updateNotificationSettings', 'updateOrderReminderSettings', 'updateDietSettings', 'updateUserPoints', 'addNotification']),
    
    // 保存设置
    saveSettings() {
      // 使用Vuex actions保存设置
      this.updateNotificationSettings(this.notificationSettings)
      this.updateOrderReminderSettings(this.orderReminderSettings)
      this.updateDietSettings(this.dietSettings)
      this.$message.success('设置已保存')
    },
    
    // 兑换奖励
    exchangeReward(reward) {
      if (this.userPoints < reward.points) {
        this.$message.error('积分不足')
        return
      }
      
      this.$confirm(`确定要用${reward.points}积分兑换${reward.name}吗？`, '兑换确认', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 使用Vuex action扣除积分
        this.updateUserPoints(-reward.points)
        
        // 添加积分变动通知
        this.addNotification({
          title: '积分变动',
          content: `兑换${reward.name}成功，扣除${reward.points}积分`,
          type: 'point',
          data: {
            '变动类型': '积分兑换',
            '积分变化': -reward.points,
            '当前积分': this.userPoints - reward.points
          }
        })
        
        this.$message.success(`兑换${reward.name}成功！`)
      }).catch(() => {
        this.$message.info('已取消兑换')
      })
    },
    
    // 更新当前实际时间
    updateCurrentRealTime() {
      const now = new Date()
      this.currentRealTime = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    },
    
    // 立即触发提醒
    testReminderNow() {
      this.$confirm('确定要立即触发点餐提醒吗？', '调试提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'info'
      }).then(() => {
        // 使用Vuex action添加测试通知
        this.addNotification({
          title: '调试提醒',
          content: '这是一个调试用的点餐提醒',
          type: 'order',
          data: {
            '测试时间': this.currentRealTime,
            '来源': '调试功能'
          },
          actions: [
            {
              id: 1,
              text: '去点餐',
              type: 'primary',
              action: 'navigate',
              target: '/foodorder/restaurants'
            }
          ]
        })
        
        // 显示调试成功提示
        this.$message.success('已触发测试提醒，可在通知中心查看')
      }).catch(() => {
        this.$message.info('已取消触发')
      })
    },
    
    // 应用模拟时间
    setDebugTime() {
      if (!this.debugTime) {
        this.$message.warning('请先选择要模拟的时间')
        return
      }
      
      // 这里可以将模拟时间保存到Vuex或localStorage，供其他组件使用
      localStorage.setItem('debugTime', this.debugTime)
      
      this.$message.success(`已设置模拟时间为 ${this.debugTime}`)
      
      // 触发一个通知，显示模拟时间已设置
      this.addNotification({
        title: '调试通知',
        content: `已设置模拟时间为 ${this.debugTime}，所有提醒将基于此时间触发`,
        type: 'system',
        data: {
          '模拟时间': this.debugTime
        }
      })
    },
    
    // 重置为当前时间
    resetDebugTime() {
      this.debugTime = null
      localStorage.removeItem('debugTime')
      this.$message.success('已重置为当前实际时间')
      
      // 触发一个通知，显示已重置
      this.addNotification({
        title: '调试通知',
        content: '已重置为当前实际时间',
        type: 'system'
      })
    }
  }
}
</script>

<style scoped>
.settings-container {
  padding: 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.settings-tabs {
  margin-top: 20px;
}

.setting-card {
  margin-bottom: 20px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.setting-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 16px;
  color: #333;
  margin: 0 0 16px 0;
  padding-bottom: 8px;
  border-bottom: 1px solid #eee;
}

.setting-description {
  color: #909399;
  font-size: 14px;
  margin-top: 8px;
}

.settings-form {
  margin-top: 20px;
}

.select-input {
  width: 100%;
  max-width: 400px;
}

.time-picker {
  width: 100%;
  max-width: 400px;
}

.mt-20 {
  margin-top: 20px;
}

.points-info {
  line-height: 1.8;
  color: #606266;
  margin-bottom: 20px;
}

.rewards-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.reward-card {
  transition: all 0.3s ease;
}

.reward-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.reward-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
}

.reward-info h4 {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: bold;
}

.reward-info p {
  margin: 0;
  font-size: 14px;
  color: #606266;
  line-height: 1.5;
}

.reward-action {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 12px;
}

.point-cost {
  font-size: 16px;
  font-weight: bold;
  color: #f56c6c;
}

.reward-action .el-button {
  min-width: 100px;
}

.about-content {
  line-height: 1.8;
}

.about-content h3 {
  margin: 0 0 16px 0;
  font-size: 18px;
  font-weight: bold;
}

.about-content p {
  margin: 8px 0;
  color: #606266;
}

/* 调试设置样式 */
.debug-buttons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-top: 16px;
}

.debug-info {
  background: #f0f9ff;
  padding: 16px;
  border-radius: 8px;
  border-left: 4px solid #409eff;
  margin-top: 16px;
}

.debug-info p {
  margin: 8px 0;
  color: #606266;
  line-height: 1.6;
}

.debug-info p:first-child {
  margin-top: 0;
}

.debug-info p:last-child {
  margin-bottom: 0;
}
</style>