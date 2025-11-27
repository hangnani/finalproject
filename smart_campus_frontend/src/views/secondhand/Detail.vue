<template>
  <div class="secondhand-detail-container">
    <h2>商品详情</h2>
    <el-card>
      <div v-if="product" class="product-detail">
        <div class="product-header">
          <h3>{{ product.name }}</h3>
          <span class="product-price">¥{{ product.price }}</span>
        </div>
        <div class="product-info">
          <div class="product-basic-info">
            <p><strong>状态：</strong>{{ product.status === 0 ? '在售' : '已售出' }}</p>
            <p><strong>发布时间：</strong>{{ formatTime(product.created_at) }}</p>
            <p><strong>联系方式：</strong>{{ product.contact }}</p>
          </div>
          <div class="product-description">
            <h4>商品描述</h4>
            <p>{{ product.description }}</p>
          </div>
        </div>
        <div class="product-actions">
          <el-button type="primary" @click="addToFavorite(product.id)">收藏</el-button>
          <el-button type="success" @click="contactSeller(product.contact)">联系卖家</el-button>
        </div>
      </div>
      <div v-else class="loading">
        <el-icon class="is-loading"><loading></loading></el-icon>
        <span>加载中...</span>
      </div>
    </el-card>
  </div>
</template>

<script>
import { Loading } from '@element-ui/icons'

export default {
  name: 'SecondhandDetail',
  components: {
    Loading
  },
  data() {
    return {
      product: null
    }
  },
  created() {
    this.getProductDetail()
  },
  methods: {
    getProductDetail() {
      const productId = this.$route.params.id
      // 这里应该调用 API 获取商品详情
      // 暂时使用模拟数据
      this.product = {
        id: productId,
        name: '《Python编程从入门到精通》',
        price: 29.99,
        status: 0,
        created_at: '2025-11-27T10:30:00',
        contact: '13800138000',
        description: '这是一本Python编程入门书籍，内容涵盖Python基础语法、面向对象编程、Web开发等，适合初学者学习。' +
                    '书籍保存完好，无缺页，无笔记，9成新。欢迎感兴趣的同学联系购买。'
      }
    },
    addToFavorite(productId) {
      this.$message.success('收藏成功！')
    },
    contactSeller(contact) {
      this.$message.info(`卖家联系方式：${contact}`)
    },
    formatTime(time) {
      return new Date(time).toLocaleString()
    }
  }
}
</script>

<style scoped>
.secondhand-detail-container {
  padding: 0;
}

.product-detail {
  padding: 20px 0;
}

.product-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ebeef5;
}

.product-header h3 {
  margin: 0;
  font-size: 24px;
  color: #303133;
}

.product-price {
  font-size: 28px;
  font-weight: bold;
  color: #f56c6c;
}

.product-info {
  margin-bottom: 20px;
}

.product-basic-info {
  margin-bottom: 20px;
}

.product-basic-info p {
  margin: 10px 0;
  font-size: 16px;
  color: #606266;
}

.product-description h4 {
  margin: 0 0 10px 0;
  font-size: 18px;
  color: #303133;
}

.product-description p {
  font-size: 16px;
  line-height: 1.8;
  color: #606266;
}

.product-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 50px 0;
  font-size: 18px;
  color: #909399;
}

.loading .el-icon {
  margin-right: 10px;
  font-size: 24px;
}
</style>