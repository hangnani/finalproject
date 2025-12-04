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
            <div v-else class="dish-image-placeholder" :style="{ background: dish.gradient }">{{ dish.name }}</div>
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
      dishes: []
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
      // 根据餐厅ID获取餐厅名称和菜品
      const restaurants = {
        1: {
          name: '学生餐厅',
          dishes: [
            {
              id: 1,
              name: '宫保鸡丁',
              description: '经典川菜，鸡肉鲜嫩，花生香脆',
              price: 18.00,
              image: '',
              gradient: 'linear-gradient(135deg, #ff6b6b, #ffa502)',
              status: 0
            },
            {
              id: 2,
              name: '鱼香肉丝',
              description: '酸甜可口，肉质鲜嫩',
              price: 16.00,
              image: '',
              gradient: 'linear-gradient(135deg, #ff8c42, #ffd23f)',
              status: 0
            },
            {
              id: 3,
              name: '麻婆豆腐',
              description: '麻辣鲜香，豆腐嫩滑',
              price: 12.00,
              image: '',
              gradient: 'linear-gradient(135deg, #ff4757, #ff6348)',
              status: 1
            },
            {
              id: 4,
              name: '回锅肉',
              description: '肥而不腻，香气四溢',
              price: 20.00,
              image: '',
              gradient: 'linear-gradient(135deg, #e67e22, #d35400)',
              status: 0
            },
            {
              id: 5,
              name: '酸辣土豆丝',
              description: '酸辣爽口，脆嫩开胃',
              price: 10.00,
              image: '',
              gradient: 'linear-gradient(135deg, #ff9ff3, #f368e0)',
              status: 0
            },
            {
              id: 6,
              name: '番茄鸡蛋汤',
              description: '清淡营养，酸甜可口',
              price: 8.00,
              image: '',
              gradient: 'linear-gradient(135deg, #ffda79, #ff9ff3)',
              status: 0
            }
          ]
        },
        2: {
          name: '教工餐厅',
          dishes: [
            {
              id: 7,
              name: '清蒸鲈鱼',
              description: '鲜美嫩滑，营养丰富',
              price: 48.00,
              image: '',
              gradient: 'linear-gradient(135deg, #74b9ff, #0984e3)',
              status: 0
            },
            {
              id: 8,
              name: '红烧肉',
              description: '肥而不腻，入口即化',
              price: 32.00,
              image: '',
              gradient: 'linear-gradient(135deg, #a29bfe, #6c5ce7)',
              status: 0
            },
            {
              id: 9,
              name: '龙井虾仁',
              description: '鲜嫩Q弹，茶香浓郁',
              price: 58.00,
              image: '',
              gradient: 'linear-gradient(135deg, #00b894, #00cec9)',
              status: 0
            },
            {
              id: 10,
              name: '清炒时蔬',
              description: '新鲜时蔬，清爽可口',
              price: 16.00,
              image: '',
              gradient: 'linear-gradient(135deg, #55efc4, #81ecec)',
              status: 0
            },
            {
              id: 11,
              name: '鲍鱼鸡汤',
              description: '浓郁鲜美，营养滋补',
              price: 68.00,
              image: '',
              gradient: 'linear-gradient(135deg, #fdcb6e, #e17055)',
              status: 0
            }
          ]
        },
        3: {
          name: '清真餐厅',
          dishes: [
            {
              id: 12,
              name: '清真牛肉面',
              description: '手工拉面，牛肉鲜嫩',
              price: 15.00,
              image: '',
              gradient: 'linear-gradient(135deg, #00b894, #00cec9)',
              status: 0
            },
            {
              id: 13,
              name: '烤羊肉串',
              description: '正宗清真风味，肉质香嫩',
              price: 28.00,
              image: '',
              gradient: 'linear-gradient(135deg, #fd79a8, #e84393)',
              status: 0
            },
            {
              id: 14,
              name: '清真手抓饭',
              description: '新疆风味，颗粒分明',
              price: 18.00,
              image: '',
              gradient: 'linear-gradient(135deg, #fdcb6e, #e17055)',
              status: 0
            },
            {
              id: 15,
              name: '清真豆腐脑',
              description: '嫩滑爽口，豆香浓郁',
              price: 6.00,
              image: '',
              gradient: 'linear-gradient(135deg, #81ecec, #00cec9)',
              status: 0
            },
            {
              id: 16,
              name: '清真包子',
              description: '手工包子，馅料十足',
              price: 12.00,
              image: '',
              gradient: 'linear-gradient(135deg, #a29bfe, #6c5ce7)',
              status: 0
            },
            {
              id: 17,
              name: '清真炒面',
              description: '筋道面条，清真配料',
              price: 16.00,
              image: '',
              gradient: 'linear-gradient(135deg, #fd79a8, #e84393)',
              status: 0
            }
          ]
        },
        4: {
          name: '西式快餐',
          dishes: [
            {
              id: 18,
              name: '经典汉堡',
              description: '双层牛肉，芝士浓郁',
              price: 25.00,
              image: '',
              gradient: 'linear-gradient(135deg, #ff6b6b, #ffa502)',
              status: 0
            },
            {
              id: 19,
              name: '香辣鸡翅',
              description: '外酥里嫩，香辣可口',
              price: 18.00,
              image: '',
              gradient: 'linear-gradient(135deg, #ff8c42, #ffd23f)',
              status: 0
            },
            {
              id: 20,
              name: '薯条',
              description: '金黄酥脆，口感绝佳',
              price: 12.00,
              image: '',
              gradient: 'linear-gradient(135deg, #fdcb6e, #feca57)',
              status: 0
            },
            {
              id: 21,
              name: '鸡肉卷',
              description: '鲜嫩鸡肉，爽口蔬菜',
              price: 22.00,
              image: '',
              gradient: 'linear-gradient(135deg, #ff9ff3, #f368e0)',
              status: 0
            },
            {
              id: 22,
              name: '可乐',
              description: '冰爽可口，夏日必备',
              price: 8.00,
              image: '',
              gradient: 'linear-gradient(135deg, #0984e3, #74b9ff)',
              status: 0
            },
            {
              id: 23,
              name: '冰淇淋',
              description: '香甜浓郁，口感细腻',
              price: 15.00,
              image: '',
              gradient: 'linear-gradient(135deg, #a29bfe, #fd79a8)',
              status: 0
            }
          ]
        }
      }
      
      // 设置餐厅名称和菜品
      const restaurant = restaurants[this.restaurantId] || restaurants[1]
      this.restaurantName = restaurant.name
      this.dishes = restaurant.dishes
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