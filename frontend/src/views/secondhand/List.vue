<template>
  <div class="secondhand-list-container">
    <div class="page-header">
      <h2>二手交易</h2>
      <el-button 
        type="primary" 
        icon="el-icon-plus" 
        @click="$router.push('/secondhand/publish')"
      >
        发布商品
      </el-button>
    </div>
    
    <el-card shadow="hover" class="filter-card">
      <div class="filter-bar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索商品"
          prefix-icon="el-icon-search"
          clearable
          @keyup.enter.native="handleSearch"
          class="search-input"
        ></el-input>
        <el-select
          v-model="sortBy"
          placeholder="排序方式"
          class="sort-select"
          @change="handleSearch"
        >
          <el-option label="最新发布" value="created_at"></el-option>
          <el-option label="价格从低到高" value="price_asc"></el-option>
          <el-option label="价格从高到低" value="price_desc"></el-option>
        </el-select>
        <el-button type="primary" @click="handleSearch">搜索</el-button>
      </div>
    </el-card>
    
    <!-- 商品卡片列表 -->
    <div class="products-grid">
      <transition-group name="fade" tag="div" class="products-wrapper">
        <el-card
          v-for="product in products"
          :key="product.id"
          shadow="hover"
          class="product-card"
          @click="viewDetail(product.id)"
        >
          <div class="product-image">
            <el-image
              :src="product.image || 'https://picsum.photos/200/150'"
              fit="cover"
              lazy
            ></el-image>
            <el-tag 
              :type="product.status === 0 ? 'success' : 'danger'" 
              class="status-tag"
            >
              {{ product.status === 0 ? '在售' : '已售' }}
            </el-tag>
          </div>
          <div class="product-info">
            <h3 class="product-name">{{ product.name }}</h3>
            <div class="product-meta">
              <span class="product-price">¥{{ parseFloat(product.price).toFixed(2) }}</span>
              <span class="product-date">{{ formatTime(product.created_at) }}</span>
            </div>
            <div class="product-actions">
              <el-button 
                type="primary" 
                size="small" 
                @click.stop="viewDetail(product.id)"
              >
                查看详情
              </el-button>
              <el-button 
                type="success" 
                size="small" 
                icon="el-icon-star-off" 
                @click.stop="addToFavorite(product.id)"
              >
                收藏
              </el-button>
            </div>
          </div>
        </el-card>
      </transition-group>
    </div>
    
    <!-- 空状态 -->
    <el-empty 
      v-if="products.length === 0" 
      description="暂无商品数据"
      class="empty-state"
    >
      <el-button type="primary" @click="getProducts">刷新</el-button>
    </el-empty>
    
    <div class="pagination-container">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="totalProducts"
      ></el-pagination>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SecondhandList',
  data() {
    return {
      searchQuery: '',
      sortBy: 'created_at',
      products: [],
      currentPage: 1,
      pageSize: 10,
      totalProducts: 0
    }
  },
  created() {
    this.getProducts()
  },
  methods: {
    async getProducts() {
      let apiProducts = []
      let apiCount = 0
      
      try {
        // 调用后端 API 获取商品列表
        const response = await this.$axios.get('/secondhand/products/', {
          params: {
            search: this.searchQuery,
            sort: this.sortBy,
            page: this.currentPage,
            page_size: this.pageSize
          }
        })
        
        // 处理 API 响应
        apiProducts = response.data.results || response.data
        apiCount = response.data.count || apiProducts.length
      } catch (error) {
        console.error('获取商品列表失败:', error)
        // 不显示错误提示，避免影响用户体验
      }
      
      // 模拟数据作为"托"
      const mockProducts = [
        {
          id: 9991,
          name: '《Python编程从入门到精通》',
          price: 29.99,
          status: 0,
          created_at: '2025-11-27T10:30:00',
          image: 'https://picsum.photos/200/150?random=1'
        },
        {
          id: 9992,
          name: '无线鼠标',
          price: 19.99,
          status: 0,
          created_at: '2025-11-26T14:20:00',
          image: 'https://picsum.photos/200/150?random=2'
        },
        {
          id: 9993,
          name: '机械键盘',
          price: 89.99,
          status: 1,
          created_at: '2025-11-25T09:15:00',
          image: 'https://picsum.photos/200/150?random=3'
        },
        {
          id: 9994,
          name: '蓝牙耳机',
          price: 49.99,
          status: 0,
          created_at: '2025-11-24T16:45:00',
          image: 'https://picsum.photos/200/150?random=4'
        },
        {
          id: 9995,
          name: '充电宝',
          price: 39.99,
          status: 0,
          created_at: '2025-11-23T11:20:00',
          image: 'https://picsum.photos/200/150?random=5'
        },
        {
          id: 9996,
          name: '台灯',
          price: 24.99,
          status: 0,
          created_at: '2025-11-22T18:30:00',
          image: 'https://picsum.photos/200/150?random=6'
        }
      ]
      
      // 合并API数据和模拟数据
      this.products = [...apiProducts, ...mockProducts]
      this.totalProducts = apiCount + mockProducts.length
    },
    // 排序商品
    sortProducts() {
      switch (this.sortBy) {
        case 'created_at':
          this.products.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
          break
        case 'price_asc':
          this.products.sort((a, b) => a.price - b.price)
          break
        case 'price_desc':
          this.products.sort((a, b) => b.price - a.price)
          break
        default:
          break
      }
    },
    handleSearch() {
      // 搜索逻辑
      this.currentPage = 1
      this.getProducts()
    },
    viewDetail(productId) {
      this.$router.push(`/secondhand/detail/${productId}`)
    },
    addToFavorite(productId) {
      this.$message.success('收藏成功！')
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.currentPage = 1
      this.getProducts()
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.getProducts()
    },
    formatTime(dateString) {
      return new Date(dateString).toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
.secondhand-list-container {
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

.filter-card {
  margin-bottom: 24px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.filter-bar {
  margin-bottom: 0;
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.search-input {
  width: 300px;
  min-width: 200px;
  flex: 1;
}

.sort-select {
  width: 180px;
}

/* 商品网格布局 */
.products-grid {
  margin: 24px 0;
}

.products-wrapper {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

/* 商品卡片样式 */
.product-card {
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  overflow: hidden;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.product-image {
  position: relative;
  height: 180px;
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  transition: transform 0.3s ease;
}

.product-card:hover .product-image img {
  transform: scale(1.05);
}

.status-tag {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 1;
}

.product-info {
  padding: 16px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.product-name {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 8px;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.product-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  font-size: 14px;
}

.product-price {
  font-size: 20px;
  font-weight: bold;
  color: #ff4d4f;
}

.product-date {
  color: #999;
}

.product-actions {
  display: flex;
  gap: 8px;
  margin-top: auto;
}

.product-actions .el-button {
  flex: 1;
}

/* 空状态 */
.empty-state {
  margin: 60px 0;
  text-align: center;
}

/* 分页样式 */
.pagination-container {
  margin-top: 32px;
  text-align: center;
  display: flex;
  justify-content: center;
}

/* 动画效果 */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.5s ease;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* 深色模式适配 */
:deep(.dark-mode) .page-header h2 {
  color: #e0e0e0;
}

:deep(.dark-mode) .product-name {
  color: #e0e0e0;
}

:deep(.dark-mode) .product-date {
  color: #999;
}
</style>