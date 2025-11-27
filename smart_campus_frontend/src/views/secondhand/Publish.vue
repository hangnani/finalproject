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
          >
            <el-option label="书籍" value="1"></el-option>
            <el-option label="电子产品" value="2"></el-option>
            <el-option label="生活用品" value="3"></el-option>
            <el-option label="运动器材" value="4"></el-option>
            <el-option label="其他" value="5"></el-option>
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
        category: '',
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
          { required: true, message: '请输入商品价格', trigger: 'blur' }
        ],
        category: [
          { required: true, message: '请选择商品分类', trigger: 'change' }
        ],
        contact: [
          { required: true, message: '请输入联系方式', trigger: 'blur' }
        ]
      },
      loading: false
    }
  },
  methods: {
    handlePublish() {
      this.$refs.publishForm.validate((valid) => {
        if (valid) {
          this.loading = true
          // 这里应该调用 API 发布商品
          setTimeout(() => {
            this.loading = false
            this.$message.success('商品发布成功！')
            this.$router.push('/secondhand/my-products')
          }, 1500)
        } else {
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