<template>
  <div class="foodorder-restaurants-container">
    <h2>餐厅列表</h2>
    <div class="restaurants-content">
      <div class="search-section">
        <el-input
          v-model="searchQuery"
          placeholder="搜索餐厅名称或地址"
          prefix-icon="el-icon-search"
          clearable
          style="width: 300px;"
        ></el-input>
      </div>
      
      <div class="restaurants-grid">
        <el-card
          v-for="restaurant in filteredRestaurants"
          :key="restaurant.id"
          class="restaurant-card"
          @click="goToDishes(restaurant.id)"
        >
          <div class="restaurant-header">
            <h3 class="restaurant-name">{{ restaurant.name }}</h3>
            <div class="restaurant-rating">
              <el-rate
                v-model="restaurant.rating"
                disabled
                :max="5"
                show-score
                text-color="#ff9900"
                score-template="{value}"
              ></el-rate>
            </div>
          </div>
          <div class="restaurant-info">
            <p class="restaurant-location"><i class="el-icon-location"></i> {{ restaurant.location }}</p>
            <p class="restaurant-hours"><i class="el-icon-time"></i> {{ restaurant.opening_hours }}</p>
            <p class="restaurant-dish-count">{{ restaurant.dish_count }} 道菜品</p>
          </div>
          <div class="restaurant-desc">{{ restaurant.description }}</div>
        </el-card>
      </div>
      
      <div v-if="filteredRestaurants.length === 0" class="empty-state">
        <el-empty description="暂无餐厅数据"></el-empty>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FoodorderRestaurants',
  data() {
    return {
      searchQuery: '',
      restaurants: [
        // 模拟数据
        {
          id: 1,
          name: '学生餐厅',
          description: '提供各种中式快餐，价格实惠，口味正宗',
          location: '学生食堂一楼',
          opening_hours: '06:30-22:00',
          dish_count: 56,
          rating: 4.5
        },
        {
          id: 2,
          name: '教工餐厅',
          description: '环境优雅，菜品精致，适合师生聚餐',
          location: '行政楼二楼',
          opening_hours: '07:00-21:30',
          dish_count: 42,
          rating: 4.8
        },
        {
          id: 3,
          name: '清真餐厅',
          description: '严格按照清真饮食规定制作，口味独特',
          location: '学生食堂二楼',
          opening_hours: '06:30-22:00',
          dish_count: 38,
          rating: 4.6
        },
        {
          id: 4,
          name: '西式快餐',
          description: '汉堡、薯条、炸鸡等西式快餐',
          location: '学生活动中心',
          opening_hours: '10:00-22:30',
          dish_count: 28,
          rating: 4.3
        }
      ]
    }
  },
  computed: {
    filteredRestaurants() {
      if (!this.searchQuery) {
        return this.restaurants
      }
      const query = this.searchQuery.toLowerCase()
      return this.restaurants.filter(restaurant => 
        restaurant.name.toLowerCase().includes(query) || 
        restaurant.location.toLowerCase().includes(query)
      )
    }
  },
  methods: {
    goToDishes(restaurantId) {
      this.$router.push(`/foodorder/dishes/${restaurantId}`)
    }
  }
}
</script>

<style scoped>
.foodorder-restaurants-container {
  padding: 20px;
}

.restaurants-content {
  max-width: 1200px;
}

.search-section {
  margin-bottom: 20px;
}

.restaurants-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.restaurant-card {
  cursor: pointer;
  transition: all 0.3s;
}

.restaurant-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.restaurant-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.restaurant-name {
  margin: 0;
  font-size: 18px;
  font-weight: bold;
}

.restaurant-rating {
  margin-left: 10px;
}

.restaurant-info {
  margin: 10px 0;
  line-height: 1.6;
  color: #606266;
}

.restaurant-location,
.restaurant-hours {
  margin: 5px 0;
  font-size: 14px;
}

.restaurant-dish-count {
  margin: 5px 0;
  font-size: 14px;
  color: #409EFF;
}

.restaurant-desc {
  font-size: 14px;
  color: #909399;
  margin-top: 10px;
  line-height: 1.5;
}

.empty-state {
  margin: 50px 0;
  text-align: center;
}
</style>