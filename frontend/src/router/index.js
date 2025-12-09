import Vue from 'vue'
import VueRouter from 'vue-router'

// 导入组件
const Login = () => import('@/views/Login.vue')
const Register = () => import('@/views/Register.vue')
const Home = () => import('@/views/Home.vue')
const Profile = () => import('@/views/Profile.vue')

// 二手交易组件
const SecondhandList = () => import('@/views/secondhand/List.vue')
const SecondhandDetail = () => import('@/views/secondhand/Detail.vue')
const SecondhandPublish = () => import('@/views/secondhand/Publish.vue')
const SecondhandMyProducts = () => import('@/views/secondhand/MyProducts.vue')
const SecondhandMessages = () => import('@/views/secondhand/Messages.vue')

// 课程表组件
const TimetableList = () => import('@/views/timetable/List.vue')
const TimetableAdd = () => import('@/views/timetable/Add.vue')
const TimetableImport = () => import('@/views/timetable/Import.vue')

// 校园点餐组件
const FoodorderRestaurants = () => import('@/views/foodorder/Restaurants.vue')
const FoodorderDishes = () => import('@/views/foodorder/Dishes.vue')
const FoodorderCart = () => import('@/views/foodorder/Cart.vue')
const FoodorderOrders = () => import('@/views/foodorder/Orders.vue')
const FoodorderOrderDetail = () => import('@/views/foodorder/OrderDetail.vue')

// 其他组件
const Settings = () => import('@/views/Settings.vue')
const Notifications = () => import('@/views/Notifications.vue')
const Dashboard = () => import('@/views/Dashboard.vue')

// 聊天组件
const ChatList = () => import('@/views/chat/List.vue')
const ChatDetail = () => import('@/views/chat/Detail.vue')

// 管理员组件
const AdminIndex = () => import('@/views/admin/Index.vue')
const AdminUsers = () => import('@/views/admin/Users.vue')
const AdminLectures = () => import('@/views/admin/Lectures.vue')
const AdminRestaurants = () => import('@/views/admin/Restaurants.vue')
const AdminExams = () => import('@/views/admin/Exams.vue')

Vue.use(VueRouter)

const routes = [
  // 公共路由
  { path: '/login', name: 'Login', component: Login, meta: { requiresAuth: false } },
  { path: '/register', name: 'Register', component: Register, meta: { requiresAuth: false } },
  
  // 主路由
  { path: '/', name: 'Home', component: Home, meta: { requiresAuth: true } },
  { path: '/profile', name: 'Profile', component: Profile, meta: { requiresAuth: true } },
  { path: '/settings', name: 'Settings', component: Settings, meta: { requiresAuth: true } },
  { path: '/notifications', name: 'Notifications', component: Notifications, meta: { requiresAuth: true } },
  { path: '/dashboard', name: 'Dashboard', component: Dashboard, meta: { requiresAuth: true } },
  
  // 二手交易路由
  { path: '/secondhand', name: 'SecondhandList', component: SecondhandList, meta: { requiresAuth: true } },
  { path: '/secondhand/detail/:id', name: 'SecondhandDetail', component: SecondhandDetail, meta: { requiresAuth: true } },
  { path: '/secondhand/publish', name: 'SecondhandPublish', component: SecondhandPublish, meta: { requiresAuth: true } },
  { path: '/secondhand/my-products', name: 'SecondhandMyProducts', component: SecondhandMyProducts, meta: { requiresAuth: true } },
  { path: '/secondhand/messages', name: 'SecondhandMessages', component: SecondhandMessages, meta: { requiresAuth: true } },
  
  // 课程表路由
  { path: '/timetable', name: 'TimetableList', component: TimetableList, meta: { requiresAuth: true } },
  { path: '/timetable/add', name: 'TimetableAdd', component: TimetableAdd, meta: { requiresAuth: true } },
  { path: '/timetable/import', name: 'TimetableImport', component: TimetableImport, meta: { requiresAuth: true } },
  
  // 校园点餐路由
  { path: '/foodorder/restaurants', name: 'FoodorderRestaurants', component: FoodorderRestaurants, meta: { requiresAuth: true } },
  { path: '/foodorder/dishes/:restaurantId', name: 'FoodorderDishes', component: FoodorderDishes, meta: { requiresAuth: true } },
  { path: '/foodorder/cart', name: 'FoodorderCart', component: FoodorderCart, meta: { requiresAuth: true } },
  { path: '/foodorder/orders', name: 'FoodorderOrders', component: FoodorderOrders, meta: { requiresAuth: true } },
  { path: '/foodorder/order/:id', name: 'FoodorderOrderDetail', component: FoodorderOrderDetail, meta: { requiresAuth: true } },
  
  // 聊天路由
  { path: '/chat', name: 'ChatList', component: ChatList, meta: { requiresAuth: true } },
  { path: '/chat/:id', name: 'ChatDetail', component: ChatDetail, meta: { requiresAuth: true } },
  
  // 管理员路由
  { path: '/admin', name: 'AdminIndex', component: AdminIndex, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/admin/users', name: 'AdminUsers', component: AdminUsers, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/admin/lectures', name: 'AdminLectures', component: AdminLectures, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/admin/restaurants', name: 'AdminRestaurants', component: AdminRestaurants, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/admin/exams', name: 'AdminExams', component: AdminExams, meta: { requiresAuth: true, requiresAdmin: true } },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 检查路由是否需要认证
  if (to.meta.requiresAuth) {
    // 检查本地存储中是否有 token
    const token = localStorage.getItem('token')
    if (token) {
      // 获取用户信息
      const userStr = localStorage.getItem('user')
      if (userStr) {
        try {
          const user = JSON.parse(userStr)
          
          // 检查是否是管理员访问设置页面
          if ((user.is_admin || user.is_staff) && to.path === '/settings') {
            // 管理员访问设置页面，重定向到管理员控制台
            next({ name: 'AdminIndex' })
            return
          }
          
          // 检查是否需要管理员权限
          if (to.meta.requiresAdmin) {
            // 检查用户是否是管理员
            if (user.is_admin || user.is_staff) {
              next()
            } else {
              // 不是管理员，跳转到首页
              next({ name: 'Home' })
              // 显示错误信息
              Vue.prototype.$message.error('您没有管理员权限')
            }
          } else {
            // 不需要管理员权限，直接放行
            next()
          }
        } catch (error) {
          console.error('解析用户信息失败:', error)
          next({ name: 'Login' })
        }
      } else {
        // 没有用户信息，跳转到登录页
        next({ name: 'Login' })
      }
    } else {
      // 没有 token，跳转到登录页
      next({ name: 'Login' })
    }
  } else {
    // 不需要认证的路由，直接放行
    next()
  }
})

export default router