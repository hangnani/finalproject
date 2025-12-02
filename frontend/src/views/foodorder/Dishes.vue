<template>
  <div class="foodorder-dishes-container">
    <div class="dishes-header">
      <el-button icon="el-icon-back" @click="$router.go(-1)">返回</el-button>
      <h2>{{ restaurantName }}</h2>
      <el-button type="primary" icon="el-icon-shopping-cart-full" @click="$router.push('/foodorder/cart')">
        购物车 ({{ cartCount }})
      </el-button>
    </div>
    
    <div class="dishes-content">
      <div class="search-section">
        <el-input
          v-model="searchQuery"
          placeholder="搜索菜品名称"
          prefix-icon="el-icon-search"
          clearable
          style="width: 300px;"
        ></el-input>
      </div>
      
      <div class="dishes-grid">
        <el-card
          v-for="dish in filteredDishes"
          :key="dish.id"
          class="dish-card"
        >
          <div class="dish-image">
            <img v-if="dish.image" :src="dish.image" :alt="dish.name">
            <div v-else class="dish-image-placeholder">{{ dish.name }}</div>
            <div v-if="dish.status === 1" class="sold-out-badge">售罄</div>
          </div>
          <div class="dish-info">
            <h3 class="dish-name">{{ dish.name }}</h3>
            <div class="dish-price">¥{{ dish.price.toFixed(2) }}</div>
            <div class="dish-desc">{{ dish.description }}</div>
            <div class="dish-actions">
              <el-button
                type="primary"
                size="small"
                :disabled="dish.status === 1"
                @click="addToCart(dish)"
              >
                <i class="el-icon-shopping-cart-plus"></i> 加入购物车
              </el-button>
            </div>
          </div>
        </el-card>
      </div>
      
      <div v-if="filteredDishes.length === 0" class="empty-state">
        <el-empty description="暂无菜品数据"></el-empty>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FoodorderDishes',
  data() {
    return {
      restaurantId: this.$route.params.restaurantId,
      restaurantName: '餐厅名称',
      searchQuery: '',
      cartCount: 0,
      dishes: [
        // 模拟数据
        {
          id: 1,
          name: '宫保鸡丁',
          description: '经典川菜，鸡肉鲜嫩，花生香脆',
          price: 18.00,
          image: '',
          status: 0
        },
        {
          id: 2,
          name: '鱼香肉丝',
          description: '酸甜可口，肉质鲜嫩',
          price: 16.00,
          image: '',
          status: 0
        },
        {
          id: 3,
          name: '麻婆豆腐',
          description: '麻辣鲜香，豆腐嫩滑',
          price: 12.00,
          image: '',
          status: 1
        },
        {
          id: 4,
          name: '回锅肉',
          description: '肥而不腻，香气四溢',
          price: 20.00,
          image: '',
          status: 0
        }
      ]
    }
  },
  computed: {
    filteredDishes() {
      if (!this.searchQuery) {
        return this.dishes
      }
      const query = this.searchQuery.toLowerCase()
      return this.dishes.filter(dish => 
        dish.name.toLowerCase().includes(query) || 
        dish.description.toLowerCase().includes(query)
      )
    }
  },
  mounted() {
    this.getRestaurantName()
    this.getCartCount()
  },
  methods: {
    getRestaurantName() {
      // 这里应该调用API获取餐厅名称
      this.restaurantName = '学生餐厅'
    },
    getCartCount() {
      // 这里应该调用API获取购物车数量
      this.cartCount = 3
    },
    addToCart(dish) {
      // 这里应该调用API添加到购物车
      this.$message.success(`${dish.name} 已加入购物车`)
      this.cartCount++
    }
  }
}
</script>

<style scoped>
.foodorder-dishes-container {
  padding: 20px;
}

.dishes-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.dishes-content {
  max-width: 1200px;
}

.search-section {
  margin-bottom: 20px;
}

.dishes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.dish-card {
  transition: all 0.3s;
}

.dish-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.dish-image {
  position: relative;
  height: 200px;
  overflow: hidden;
  border-radius: 4px;
}

.dish-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.dish-image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
  color: #909399;
  font-size: 18px;
  font-weight: bold;
}

.sold-out-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(255, 0, 0, 0.8);
  color: white;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.dish-info {
  padding: 10px 0;
}

.dish-name {
  margin: 0 0 10px 0;
  font-size: 16px;
  font-weight: bold;
}

.dish-price {
  color: #f56c6c;
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
}

.dish-desc {
  color: #606266;
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 15px;
  height: 45px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.dish-actions {
  text-align: right;
}

.empty-state {
  margin: 50px 0;
  text-align: center;
}
</style>