<template>
  <div class="foodorder-restaurants-container">
    <div class="page-header">
      <h2>餐厅列表</h2>
    </div>
    <div class="restaurants-content">
      <el-card shadow="hover" class="filter-card">
        <div class="filter-bar">
          <el-input v-model="searchQuery" placeholder="搜索餐厅名称或地址" prefix-icon="el-icon-search" clearable @keyup.enter.native="handleSearch" class="search-input"></el-input>
          <el-select v-model="sortBy" placeholder="排序方式" class="sort-select" @change="handleSearch">
            <el-option label="综合评分" value="rating_desc"></el-option>
            <el-option label="菜品数量" value="dish_count_desc"></el-option>
            <el-option label="名称排序" value="name_asc"></el-option>
          </el-select>
        </div>
      </el-card>
      
      <!-- 餐厅卡片列表 -->
      <div class="restaurants-grid">
        <transition-group name="fade" tag="div" class="restaurants-wrapper">
          <el-card v-for="restaurant in filteredRestaurants" :key="restaurant.id" class="restaurant-card" shadow="hover" @click="goToDishes(restaurant.id)">
            <div class="restaurant-banner">
              <div class="restaurant-image">
                <!-- 使用内联样式的渐变色代替外部图片，避免ORB阻止 -->
                <div class="restaurant-image-placeholder" :style="{ background: getGradientColor(restaurant.id) }"></div>
                <div class="restaurant-badge" v-if="restaurant.is_open">
                  <el-tag type="success">营业中</el-tag>
                </div>
                <div class="restaurant-badge" v-else>
                  <el-tag type="danger">已打烊</el-tag>
                </div>
              </div>
            </div>
            
            <div class="restaurant-header">
              <h3 class="restaurant-name">{{ restaurant.name }}</h3>
              <div class="restaurant-rating">
                <el-rate v-model="restaurant.rating" disabled :max="5" show-score text-color="#ff9900" score-template="{value}"></el-rate>
              </div>
            </div>
            
            <div class="restaurant-info">
              <div class="info-item">
                <i class="el-icon-location"></i>
                <span>{{ restaurant.location }}</span>
              </div>
              <div class="info-item">
                <i class="el-icon-time"></i>
                <span>{{ restaurant.opening_hours }}</span>
              </div>
              <div class="info-item">
                <i class="el-icon-s-goods"></i>
                <span>{{ restaurant.dish_count }} 道菜品</span>
              </div>
            </div>
            
            <div class="restaurant-desc">{{ restaurant.description }}</div>
            
            <div class="restaurant-actions">
              <el-button type="primary" @click.stop="goToDishes(restaurant.id)">查看菜品</el-button>
            </div>
          </el-card>
        </transition-group>
      </div>
      
      <div v-if="filteredRestaurants.length === 0" class="empty-state">
        <el-empty description="暂无餐厅数据">
          <el-button type="primary" @click="refreshRestaurants">刷新</el-button>
        </el-empty>
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
      sortBy: 'rating_desc',
      restaurants: [
        {
          id: 1,
          name: '学生餐厅',
          description: '提供各种中式快餐，价格实惠，口味正宗',
          location: '学生食堂一楼',
          opening_hours: '06:30-22:00',
          dish_count: 56,
          rating: 4.5,
          is_open: true
        },
        {
          id: 2,
          name: '教工餐厅',
          description: '环境优雅，菜品精致，适合师生聚餐',
          location: '行政楼二楼',
          opening_hours: '07:00-21:30',
          dish_count: 42,
          rating: 4.8,
          is_open: true
        },
        {
          id: 3,
          name: '清真餐厅',
          description: '严格按照清真饮食规定制作，口味独特',
          location: '学生食堂二楼',
          opening_hours: '06:30-22:00',
          dish_count: 38,
          rating: 4.6,
          is_open: true
        },
        {
          id: 4,
          name: '西式快餐',
          description: '汉堡、薯条、炸鸡等西式快餐',
          location: '学生活动中心',
          opening_hours: '10:00-22:30',
          dish_count: 28,
          rating: 4.3,
          is_open: true
        }
      ]
    }
  },
  computed: {
    filteredRestaurants() {
      let restaurants = [...this.restaurants]
      
      // 搜索过滤
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        restaurants = restaurants.filter(restaurant => {
          return restaurant.name.toLowerCase().includes(query) || restaurant.location.toLowerCase().includes(query)
        })
      }
      
      // 排序
      switch (this.sortBy) {
        case 'rating_desc':
          restaurants.sort((a, b) => b.rating - a.rating)
          break
        case 'dish_count_desc':
          restaurants.sort((a, b) => b.dish_count - a.dish_count)
          break
        case 'name_asc':
          restaurants.sort((a, b) => a.name.localeCompare(b.name))
          break
        default:
          break
      }
      
      return restaurants
    }
  },
  methods: {
    goToDishes(restaurantId) {
      this.$router.push(`/foodorder/dishes/${restaurantId}`)
    },
    handleSearch() {
      // 搜索逻辑
    },
    refreshRestaurants() {
      this.$message.success('餐厅数据已刷新')
    },
    getGradientColor(id) {
      // 基于餐厅ID生成不同的渐变色，避免使用外部图片
      const gradients = [
        'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
        'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
        'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
        'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
        'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
        'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)',
        'linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%)'
      ]
      return gradients[id % gradients.length]
    }
  }
}
</script>

<style scoped>
.foodorder-restaurants-container {
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

.restaurants-content {
  max-width: 100%;
}

.filter-card {
  margin-bottom: 24px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.filter-bar {
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

.restaurants-grid {
  margin: 24px 0;
}

.restaurants-wrapper {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
}

.restaurant-card {
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 8px;
  overflow: hidden;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.restaurant-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
}

.restaurant-banner {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.restaurant-image {
  position: relative;
  height: 100%;
  width: 100%;
}

.restaurant-image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s ease;
}

.restaurant-card:hover .restaurant-image-placeholder {
  transform: scale(1.05);
}

.restaurant-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 10;
}

.restaurant-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
  padding: 0 16px;
}

.restaurant-name {
  font-size: 18px;
  font-weight: bold;
  margin: 16px 0 0 0;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 200px;
}

.restaurant-rating {
  margin-top: 16px;
  margin-left: 0;
}

.restaurant-info {
  padding: 0 16px;
  margin-bottom: 12px;
  margin: 0 0 12px 0;
  line-height: 1.6;
  color: #606266;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
  margin: 8px 0;
  line-height: 1.5;
}

.restaurant-desc {
  padding: 0 16px 16px;
  font-size: 14px;
  color: #909399;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  margin-bottom: auto;
  margin: 0 0 16px 0;
  line-height: 1.5;
}

.restaurant-actions {
  padding: 0 16px 16px;
  display: flex;
  gap: 8px;
}

.restaurant-actions .el-button {
  flex: 1;
}

.empty-state {
  margin: 60px 0;
  text-align: center;
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.5s ease;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

:deep(.dark-mode) .page-header h2 {
  color: #e0e0e0;
}

:deep(.dark-mode) .restaurant-name {
  color: #e0e0e0;
}

:deep(.dark-mode) .info-item {
  color: #999;
}

:deep(.dark-mode) .restaurant-desc {
  color: #888;
}
</style>
