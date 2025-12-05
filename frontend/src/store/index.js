import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    // 用户信息
    user: JSON.parse(localStorage.getItem('user')) || null,
    token: localStorage.getItem('token') || null,
    // 主题模式: light/dark
    theme: localStorage.getItem('theme') || 'light',
    // 购物车商品
    cart: JSON.parse(localStorage.getItem('cart')) || [],
    // 通知列表
    notifications: JSON.parse(localStorage.getItem('notifications')) || [],
    // 用户设置
    settings: JSON.parse(localStorage.getItem('settings')) || {
      // 通知设置
      notificationSettings: {
        courseReminders: true,
        orderNotifications: true,
        secondhandMessages: true,
        pointNotifications: true
      },
      // 点餐提醒设置
      orderReminderSettings: {
        classReminders: true,
        freeTimeReminders: true,
        reminderTimes: ['11:00', '17:00']
      },
      // 饮食偏好设置
      dietSettings: {
        tabooIngredients: [],
        preferredTypes: [],
        pricePreference: 3
      }
    },
    // 用户积分
    userPoints: parseInt(localStorage.getItem('userPoints')) || 1000
  },
  getters: {
    isLoggedIn: state => !!state.token,
    currentUser: state => state.user,
    isDarkMode: state => state.theme === 'dark',
    cartCount: state => state.cart.reduce((total, item) => total + item.quantity, 0),
    cartTotal: state => state.cart.reduce((total, item) => total + (item.price * item.quantity), 0),
    // 通知相关getters
    unreadCount: state => state.notifications.filter(notification => !notification.read).length,
    allNotifications: state => state.notifications.sort((a, b) => new Date(b.created_at) - new Date(a.created_at)),
    unreadNotifications: state => state.notifications.filter(notification => !notification.read).sort((a, b) => new Date(b.created_at) - new Date(a.created_at)),
    // 设置相关getters
    notificationSettings: state => state.settings.notificationSettings,
    orderReminderSettings: state => state.settings.orderReminderSettings,
    dietSettings: state => state.settings.dietSettings
  },
  mutations: {
    // 设置用户信息
    SET_USER(state, user) {
      state.user = user
      localStorage.setItem('user', JSON.stringify(user))
    },
    // 设置token
    SET_TOKEN(state, token) {
      state.token = token
      localStorage.setItem('token', token)
    },
    // 退出登录
    LOGOUT(state) {
      state.user = null
      state.token = null
      localStorage.removeItem('user')
      localStorage.removeItem('token')
    },
    // 切换主题
    TOGGLE_THEME(state) {
      state.theme = state.theme === 'light' ? 'dark' : 'light'
      localStorage.setItem('theme', state.theme)
    },
    // 设置主题
    SET_THEME(state, theme) {
      state.theme = theme
      localStorage.setItem('theme', theme)
    },
    // 添加商品到购物车
    ADD_TO_CART(state, product) {
      const existingItem = state.cart.find(item => item.id === product.id)
      if (existingItem) {
        existingItem.quantity++
      } else {
        state.cart.push({ ...product, quantity: 1 })
      }
      localStorage.setItem('cart', JSON.stringify(state.cart))
    },
    // 更新购物车商品数量
    UPDATE_CART_QUANTITY(state, { id, quantity }) {
      const item = state.cart.find(item => item.id === id)
      if (item) {
        item.quantity = quantity
        if (item.quantity <= 0) {
          state.cart = state.cart.filter(item => item.id !== id)
        }
        localStorage.setItem('cart', JSON.stringify(state.cart))
      }
    },
    // 从购物车移除商品
    REMOVE_FROM_CART(state, id) {
      state.cart = state.cart.filter(item => item.id !== id)
      localStorage.setItem('cart', JSON.stringify(state.cart))
    },
    // 清空购物车
    CLEAR_CART(state) {
      state.cart = []
      localStorage.setItem('cart', JSON.stringify(state.cart))
    },
    // 通知相关mutations
    ADD_NOTIFICATION(state, notification) {
      // 生成唯一ID
      const id = Date.now() + Math.random().toString(36).substr(2, 9)
      const newNotification = {
        id,
        read: false,
        created_at: new Date().toISOString(),
        ...notification
      }
      // 添加到通知列表开头
      state.notifications.unshift(newNotification)
      // 限制通知数量，最多保存100条
      if (state.notifications.length > 100) {
        state.notifications = state.notifications.slice(0, 100)
      }
      localStorage.setItem('notifications', JSON.stringify(state.notifications))
    },
    MARK_NOTIFICATION_READ(state, notificationId) {
      const notification = state.notifications.find(n => n.id === notificationId)
      if (notification) {
        notification.read = true
        localStorage.setItem('notifications', JSON.stringify(state.notifications))
      }
    },
    MARK_ALL_NOTIFICATIONS_READ(state) {
      state.notifications.forEach(notification => {
        notification.read = true
      })
      localStorage.setItem('notifications', JSON.stringify(state.notifications))
    },
    CLEAR_ALL_NOTIFICATIONS(state) {
      state.notifications = []
      localStorage.setItem('notifications', JSON.stringify(state.notifications))
    },
    REMOVE_NOTIFICATION(state, notificationId) {
      state.notifications = state.notifications.filter(n => n.id !== notificationId)
      localStorage.setItem('notifications', JSON.stringify(state.notifications))
    },
    // 设置相关mutations
    UPDATE_SETTINGS(state, newSettings) {
      state.settings = { ...state.settings, ...newSettings }
      localStorage.setItem('settings', JSON.stringify(state.settings))
    },
    UPDATE_NOTIFICATION_SETTINGS(state, notificationSettings) {
      state.settings.notificationSettings = { ...state.settings.notificationSettings, ...notificationSettings }
      localStorage.setItem('settings', JSON.stringify(state.settings))
    },
    UPDATE_ORDER_REMINDER_SETTINGS(state, orderReminderSettings) {
      state.settings.orderReminderSettings = { ...state.settings.orderReminderSettings, ...orderReminderSettings }
      localStorage.setItem('settings', JSON.stringify(state.settings))
    },
    UPDATE_DIET_SETTINGS(state, dietSettings) {
      state.settings.dietSettings = { ...state.settings.dietSettings, ...dietSettings }
      localStorage.setItem('settings', JSON.stringify(state.settings))
    },
    // 积分相关mutations
    UPDATE_USER_POINTS(state, points) {
      state.userPoints += points
      localStorage.setItem('userPoints', state.userPoints.toString())
    },
    SET_USER_POINTS(state, points) {
      state.userPoints = points
      localStorage.setItem('userPoints', state.userPoints.toString())
    }
  },
  actions: {
    // 登录
    login({ commit }, { token, user }) {
      commit('SET_TOKEN', token)
      commit('SET_USER', user)
    },
    // 退出登录
    logout({ commit }) {
      commit('LOGOUT')
    },
    // 切换主题
    toggleTheme({ commit }) {
      commit('TOGGLE_THEME')
    },
    // 设置主题
    setTheme({ commit }, theme) {
      commit('SET_THEME', theme)
    },
    // 添加到购物车
    addToCart({ commit }, product) {
      commit('ADD_TO_CART', product)
    },
    // 更新购物车数量
    updateCartQuantity({ commit }, payload) {
      commit('UPDATE_CART_QUANTITY', payload)
    },
    // 移除购物车商品
    removeFromCart({ commit }, id) {
      commit('REMOVE_FROM_CART', id)
    },
    // 清空购物车
    clearCart({ commit }) {
      commit('CLEAR_CART')
    },
    // 通知相关actions
    addNotification({ commit }, notification) {
      commit('ADD_NOTIFICATION', notification)
    },
    markNotificationRead({ commit }, notificationId) {
      commit('MARK_NOTIFICATION_READ', notificationId)
    },
    markAllNotificationsRead({ commit }) {
      commit('MARK_ALL_NOTIFICATIONS_READ')
    },
    clearAllNotifications({ commit }) {
      commit('CLEAR_ALL_NOTIFICATIONS')
    },
    removeNotification({ commit }, notificationId) {
      commit('REMOVE_NOTIFICATION', notificationId)
    },
    // 设置相关actions
    updateSettings({ commit }, newSettings) {
      commit('UPDATE_SETTINGS', newSettings)
    },
    updateNotificationSettings({ commit }, notificationSettings) {
      commit('UPDATE_NOTIFICATION_SETTINGS', notificationSettings)
    },
    updateOrderReminderSettings({ commit }, orderReminderSettings) {
      commit('UPDATE_ORDER_REMINDER_SETTINGS', orderReminderSettings)
    },
    updateDietSettings({ commit }, dietSettings) {
      commit('UPDATE_DIET_SETTINGS', dietSettings)
    },
    // 积分相关actions
    updateUserPoints({ commit }, points) {
      commit('UPDATE_USER_POINTS', points)
    },
    setUserPoints({ commit }, points) {
      commit('SET_USER_POINTS', points)
    }
  }
})
