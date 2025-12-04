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
    cart: JSON.parse(localStorage.getItem('cart')) || []
  },
  getters: {
    isLoggedIn: state => !!state.token,
    currentUser: state => state.user,
    isDarkMode: state => state.theme === 'dark',
    cartCount: state => state.cart.reduce((total, item) => total + item.quantity, 0),
    cartTotal: state => state.cart.reduce((total, item) => total + (item.price * item.quantity), 0)
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
    }
  }
})
