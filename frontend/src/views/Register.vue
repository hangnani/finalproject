<template>
  <div class="register-container">
    <el-card class="register-card">
      <div slot="header" class="register-header">
        <h2>智能校园生活助手</h2>
        <p>创建您的账号</p>
      </div>
      
      <el-form
        ref="registerForm"
        :model="registerForm"
        :rules="registerRules"
        label-position="top"
        class="register-form"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="registerForm.username"
            placeholder="请输入用户名"
            prefix-icon="el-icon-user"
            autocomplete="off"
          ></el-input>
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="registerForm.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="el-icon-lock"
            show-password
            autocomplete="off"
          ></el-input>
        </el-form-item>
        
        <el-form-item label="确认密码" prop="password_confirm">
          <el-input
            v-model="registerForm.password_confirm"
            type="password"
            placeholder="请再次输入密码"
            prefix-icon="el-icon-lock"
            show-password
            autocomplete="off"
          ></el-input>
        </el-form-item>
        
        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="registerForm.email"
            type="email"
            placeholder="请输入邮箱"
            prefix-icon="el-icon-message"
            autocomplete="off"
          ></el-input>
        </el-form-item>
        
        <el-form-item label="姓名" prop="name">
          <el-input
            v-model="registerForm.name"
            placeholder="请输入真实姓名"
            prefix-icon="el-icon-document-copy"
            autocomplete="off"
          ></el-input>
        </el-form-item>
        
        <el-form-item label="学号" prop="student_id">
          <el-input
            v-model="registerForm.student_id"
            placeholder="请输入学号"
            prefix-icon="el-icon-document-checked"
            autocomplete="off"
          ></el-input>
        </el-form-item>
        
        <el-form-item label="手机号" prop="phone">
          <el-input
            v-model="registerForm.phone"
            placeholder="请输入手机号"
            prefix-icon="el-icon-phone"
            autocomplete="off"
          ></el-input>
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            class="register-button"
            @click="handleRegister"
            :loading="loading"
          >
            注册
          </el-button>
        </el-form-item>
        
        <div class="register-footer">
          <span>已有账号？</span>
          <el-button type="text" @click="$router.push('/login')">立即登录</el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'Register',
  data() {
    return {
      registerForm: {
        username: '',
        password: '',
        password_confirm: '',
        email: '',
        name: '',
        student_id: '',
        phone: ''
      },
      registerRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
        ],
        password_confirm: [
          { required: true, message: '请再次输入密码', trigger: 'blur' },
          { validator: this.validatePassword, trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' },
          { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
        ],
        name: [
          { required: true, message: '请输入姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '姓名长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        student_id: [
          { required: true, message: '请输入学号', trigger: 'blur' },
          { min: 6, max: 20, message: '学号长度在 6 到 20 个字符', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入手机号', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号', trigger: 'blur' }
        ]
      },
      loading: false
    }
  },
  methods: {
    validatePassword(rule, value, callback) {
      if (value !== this.registerForm.password) {
        callback(new Error('两次输入的密码不一致'))
      } else {
        callback()
      }
    },
    handleRegister() {
      this.$refs.registerForm.validate((valid) => {
        if (valid) {
          this.loading = true
          // 调用注册 API
          this.$axios.post('/users/register/', this.registerForm)
            .then(response => {
              const { user, access: token } = response.data
              // 保存到Vuex
              this.$store.dispatch('login', { user, token })
              // 跳转到首页
              this.$router.push('/')
              this.$message.success('注册成功！')
            })
            .catch(error => {
              console.error('注册失败:', error)
              this.$message.error('注册失败，请检查输入信息！')
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
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f7fa;
}

.register-card {
  width: 500px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.register-header {
  text-align: center;
  padding: 20px 0;
}

.register-header h2 {
  margin: 0 0 10px 0;
  color: #409EFF;
}

.register-header p {
  margin: 0;
  color: #909399;
}

.register-form {
  padding: 0 20px 20px 20px;
}

.register-button {
  width: 100%;
  padding: 12px 0;
  font-size: 16px;
}

.register-footer {
  text-align: center;
  margin-top: 10px;
  color: #909399;
}

.register-footer .el-button {
  padding: 0;
  font-size: 14px;
  color: #409EFF;
}
</style>