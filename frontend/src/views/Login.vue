<template>
  <div class="login-container">
    <el-card class="login-card">
      <div slot="header" class="login-header">
        <h2>智能校园生活助手</h2>
        <p>登录您的账号</p>
      </div>
      
      <el-form
        ref="loginForm"
        :model="loginForm"
        :rules="loginRules"
        label-position="top"
        class="login-form"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            prefix-icon="el-icon-user"
            autocomplete="off"
            @input="handleUsernameChange"
          ></el-input>
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="el-icon-lock"
            show-password
            autocomplete="off"
          ></el-input>
        </el-form-item>
        
        <el-form-item>
          <el-checkbox v-model="loginForm.rememberMe" class="remember-me">记住账号</el-checkbox>
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            class="login-button"
            @click="handleLogin"
            :loading="loading"
          >
            登录
          </el-button>
        </el-form-item>
        
        <div class="login-footer">
          <span>还没有账号？</span>
          <el-button type="text" @click="$router.push('/register')">立即注册</el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      loginForm: {
        username: '',
        password: '',
        rememberMe: false
      },
      loginRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
        ]
      },
      loading: false,
      // 保存的账号密码字典
      savedCredentials: {}
    }
  },
  created() {
    // 从localStorage中读取保存的账号密码字典
    this.loadSavedCredentials()
    
    // 设置默认勾选状态
    this.loginForm.rememberMe = Object.keys(this.savedCredentials).length > 0
  },
  methods: {
    loadSavedCredentials() {
      // 读取保存的账号密码字典
      const saved = localStorage.getItem('savedCredentials')
      if (saved) {
        try {
          this.savedCredentials = JSON.parse(saved)
        } catch (e) {
          console.error('解析保存的凭据失败:', e)
          this.savedCredentials = {}
        }
      }
    },
    saveCredentials() {
      // 保存账号密码字典到localStorage
      localStorage.setItem('savedCredentials', JSON.stringify(this.savedCredentials))
    },
    handleUsernameChange() {
      // 用户名变化时，自动填入对应的密码
      if (this.savedCredentials[this.loginForm.username]) {
        this.loginForm.password = this.savedCredentials[this.loginForm.username]
      } else {
        this.loginForm.password = ''
      }
    },
    handleLogin() {
      this.$refs.loginForm.validate((valid) => {
        if (valid) {
          this.loading = true
          // 调用登录 API
          this.$axios.post('/users/login/', this.loginForm)
            .then(response => {
              const { user, access: token } = response.data
              
              // 根据用户选择保存用户名和密码到字典
              if (this.loginForm.rememberMe) {
                // 将当前账号密码添加到保存的凭据字典中
                this.savedCredentials[this.loginForm.username] = this.loginForm.password
                // 保存字典到localStorage
                this.saveCredentials()
              } else {
                // 移除当前账号的保存记录
                if (this.savedCredentials[this.loginForm.username]) {
                  delete this.savedCredentials[this.loginForm.username]
                  this.saveCredentials()
                }
              }
              
              // 保存到Vuex
              this.$store.dispatch('login', { user, token })
              
              // 根据用户角色跳转到不同页面
              if (user.is_admin || user.is_staff) {
                // 管理员跳转到管理员控制台
                this.$router.push('/admin')
                this.$message.success('管理员登录成功！')
              } else {
                // 普通用户跳转到首页
                this.$router.push('/')
                this.$message.success('登录成功！')
              }
            })
            .catch(error => {
              console.error('登录失败:', error)
              this.$message.error('登录失败，请检查用户名和密码！')
            })
            .finally(() => {
              this.loading = false
            })
        } else {
          return false
        }
      })
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f7fa;
}

.login-card {
  width: 400px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.login-header {
  text-align: center;
  padding: 20px 0;
}

.login-header h2 {
  margin: 0 0 10px 0;
  color: #409EFF;
}

.login-header p {
  margin: 0;
  color: #909399;
}

.login-form {
  padding: 0 20px 20px 20px;
}

.login-button {
  width: 100%;
  padding: 12px 0;
  font-size: 16px;
}

.login-footer {
  text-align: center;
  margin-top: 10px;
  color: #909399;
}

.login-footer .el-button {
  padding: 0;
  font-size: 14px;
  color: #409EFF;
}
</style>