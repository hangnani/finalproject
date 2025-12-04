<template>
  <div class="secondhand-publish-container">
    <h2>发布二手商品</h2>
    <el-card>
      <el-form
        ref="publishForm"
        :model="publishForm"
        :rules="publishRules"
        label-position="top"
        class="publish-form"
      >
        <el-form-item label="商品名称" prop="name">
          <el-input
            v-model="publishForm.name"
            placeholder="请输入商品名称"
            autocomplete="off"
          ></el-input>
        </el-form-item>
        
        <el-form-item label="商品描述" prop="description">
          <el-input
            v-model="publishForm.description"
            type="textarea"
            :rows="5"
            placeholder="请输入商品描述"
            autocomplete="off"
          ></el-input>
        </el-form-item>
        
        <el-form-item label="商品价格" prop="price">
          <el-input-number
            v-model="publishForm.price"
            :min="0.01"
            :step="0.01"
            :precision="2"
            placeholder="请输入商品价格"
          ></el-input-number>
        </el-form-item>
        
        <el-form-item label="商品分类" prop="category">
          <el-select
            v-model="publishForm.category"
            placeholder="请选择商品分类"
            required
          >
            <el-option label="书籍" :value="1"></el-option>
            <el-option label="电子产品" :value="2"></el-option>
            <el-option label="生活用品" :value="3"></el-option>
            <el-option label="运动器材" :value="4"></el-option>
            <el-option label="其他" :value="5"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="联系方式" prop="contact">
          <el-input
            v-model="publishForm.contact"
            placeholder="请输入联系方式"
            autocomplete="off"
          ></el-input>
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            class="publish-button"
            @click="handlePublish"
            :loading="loading"
          >
            发布商品
          </el-button>
          <el-button @click="$router.go(-1)">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'SecondhandPublish',
  data() {
    return {
      publishForm: {
        name: '',
        description: '',
        price: 0,
        category: 0,
        status: 0, // 0:在售, 1:已售出
        images: [],
        contact: ''
      },
      publishRules: {
        name: [
          { required: true, message: '请输入商品名称', trigger: 'blur' },
          { min: 2, max: 100, message: '商品名称长度在 2 到 100 个字符', trigger: 'blur' }
        ],
        description: [
          { required: true, message: '请输入商品描述', trigger: 'blur' },
          { min: 10, max: 500, message: '商品描述长度在 10 到 500 个字符', trigger: 'blur' }
        ],
        price: [
          { required: true, message: '请输入商品价格', trigger: 'blur' },
          { type: 'number', min: 0.01, message: '商品价格必须大于0', trigger: 'blur' }
        ],
        category: [
          { required: true, message: '请选择商品分类', trigger: 'change' },
          { type: 'number', message: '商品分类必须是数字', trigger: 'change' }
        ],
        contact: [
          { required: true, message: '请输入联系方式', trigger: 'blur' },
          { min: 5, max: 20, message: '联系方式长度在 5 到 20 个字符', trigger: 'blur' }
        ]
      },
      loading: false
    }
  },
  methods: {
    async handlePublish() {
      this.$refs.publishForm.validate(async (valid) => {
        if (valid) {
          this.loading = true
          try {
            console.log('开始发布商品，表单数据:', this.publishForm)
            console.log('Token:', localStorage.getItem('token'))
            
            // 调用后端 API 发布商品
            const response = await this.$axios.post('/secondhand/products/', this.publishForm)
            
            console.log('商品发布成功，响应:', response.data)
            this.loading = false
            this.$message.success('商品发布成功！')
            
            // 跳转到我的发布页面
            this.$router.push('/secondhand/my-products')
          } catch (error) {
            this.loading = false
            console.error('发布商品失败:', error)
            
            // 显示详细的错误信息
            let errorMsg = '发布商品失败，请稍后重试'
            if (error.response) {
              // 服务器返回了错误响应
              console.error('错误响应:', error.response.data)
              console.error('错误状态码:', error.response.status)
              
              if (error.response.data) {
                if (typeof error.response.data === 'string') {
                  errorMsg = error.response.data
                } else if (error.response.data.detail) {
                  errorMsg = error.response.data.detail
                } else if (error.response.data.non_field_errors) {
                  errorMsg = error.response.data.non_field_errors[0]
                } else {
                  // 尝试获取字段错误
                  const fieldErrors = Object.values(error.response.data)
                  if (fieldErrors.length > 0) {
                    errorMsg = fieldErrors[0] instanceof Array ? fieldErrors[0][0] : fieldErrors[0]
                  }
                }
              }
            } else if (error.request) {
              // 请求已发送但没有收到响应
              errorMsg = '服务器无响应，请检查网络连接'
              console.error('请求:', error.request)
            } else {
              // 请求配置错误
              errorMsg = `请求错误: ${error.message}`
            }
            
            this.$message.error(errorMsg)
          }
        } else {
          console.error('表单验证失败')
          this.$message.warning('请检查表单填写是否完整')
          return false
        }
      })
    }
  }
}
</script>

<style scoped>
.secondhand-publish-container {
  padding: 0;
}

.publish-form {
  padding: 0 20px 20px 20px;
}

.publish-button {
  margin-right: 10px;
}
</style>