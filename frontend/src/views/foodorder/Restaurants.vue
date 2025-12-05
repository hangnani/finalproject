<template>
  <div class="foodorder-restaurants-container">
    <div class="page-header">
      <h2>餐厅列表</h2>
    </div>
    
    <!-- 饮食推荐区域 -->
    <div class="recommendation-section">
      <h3 class="section-title">今日推荐</h3>
      <el-card shadow="hover" class="recommendation-card">
        <div class="recommendation-content">
          <div class="recommendation-item" v-for="recommendation in todayRecommendations" :key="recommendation.id">
            <div class="recommendation-image" :style="{ background: getGradientColor(recommendation.restaurant_id) }"></div>
            <div class="recommendation-info">
              <h4>{{ recommendation.dish_name }}</h4>
              <p class="restaurant-name">{{ recommendation.restaurant_name }}</p>
              <div class="recommendation-meta">
                <span class="price">¥{{ recommendation.price }}</span>
                <span class="rating"><el-rate v-model="recommendation.rating" disabled :max="5" :show-score="false" text-color="#ff9900" size="small"></el-rate></span>
                <span class="sales">月售{{ recommendation.monthly_sales }}份</span>
              </div>
              <el-button type="primary" size="small" @click="goToDishes(recommendation.restaurant_id)">立即点餐</el-button>
            </div>
          </div>
        </div>
      </el-card>
      
      <!-- 性价比推荐 -->
      <h3 class="section-title mt-20">性价比推荐</h3>
      <el-card shadow="hover" class="recommendation-card">
        <div class="recommendation-content">
          <div class="recommendation-item" v-for="recommendation in costEffectiveRecommendations" :key="recommendation.id">
            <div class="recommendation-image" :style="{ background: getGradientColor(recommendation.restaurant_id) }"></div>
            <div class="recommendation-info">
              <h4>{{ recommendation.dish_name }}</h4>
              <p class="restaurant-name">{{ recommendation.restaurant_name }}</p>
              <div class="recommendation-meta">
                <span class="price">¥{{ recommendation.price }}</span>
                <span class="rating"><el-rate v-model="recommendation.rating" disabled :max="5" :show-score="false" text-color="#ff9900" size="small"></el-rate></span>
                <span class="cost-effective">性价比: {{ recommendation.cost_effective_score }}分</span>
              </div>
              <el-button type="primary" size="small" @click="goToDishes(recommendation.restaurant_id)">立即点餐</el-button>
            </div>
          </div>
        </div>
      </el-card>
    </div>
    
    <div class="restaurants-content">
      <el-card shadow="hover" class="filter-card">
        <div class="filter-bar">
          <el-input v-model="searchQuery" placeholder="搜索餐厅名称、地址或食材" prefix-icon="el-icon-search" clearable @keyup.enter.native="handleSearch" class="search-input"></el-input>
          <el-select v-model="sortBy" placeholder="排序方式" class="sort-select" @change="handleSearch">
            <el-option label="综合评分" value="rating_desc"></el-option>
            <el-option label="菜品数量" value="dish_count_desc"></el-option>
            <el-option label="名称排序" value="name_asc"></el-option>
            <el-option label="价格从低到高" value="price_asc"></el-option>
            <el-option label="价格从高到低" value="price_desc"></el-option>
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
              <div class="info-item" v-if="restaurant.specialty">
                <i class="el-icon-medal"></i>
                <span>特色: {{ restaurant.specialty }}</span>
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
      // 餐厅数据
      restaurants: [
        {
          id: 1,
          name: '学生餐厅',
          description: '提供各种中式快餐，价格实惠，口味正宗',
          location: '学生食堂一楼',
          opening_hours: '06:30-22:00',
          dish_count: 56,
          rating: 4.5,
          is_open: true,
          specialty: '中式快餐',
          average_price: 15,
          // 添加每周开放时间（1-5表示周一到周五，6-7表示周六到周日）
          opening_days: [1, 2, 3, 4, 5, 6, 7],
          // 特色食材
          ingredients: ['米饭', '面条', '蔬菜', '肉类', '鸡蛋']
        },
        {
          id: 2,
          name: '教工餐厅',
          description: '环境优雅，菜品精致，适合师生聚餐',
          location: '行政楼二楼',
          opening_hours: '07:00-21:30',
          dish_count: 42,
          rating: 4.8,
          is_open: true,
          specialty: '精致中餐',
          average_price: 25,
          opening_days: [1, 2, 3, 4, 5],
          ingredients: ['海鲜', '肉类', '蔬菜', '米饭', '汤品']
        },
        {
          id: 3,
          name: '清真餐厅',
          description: '严格按照清真饮食规定制作，口味独特',
          location: '学生食堂二楼',
          opening_hours: '06:30-22:00',
          dish_count: 38,
          rating: 4.6,
          is_open: true,
          specialty: '清真美食',
          average_price: 18,
          opening_days: [1, 2, 3, 4, 5, 6, 7],
          ingredients: ['牛肉', '羊肉', '面条', '米饭', '蔬菜']
        },
        {
          id: 4,
          name: '西式快餐',
          description: '汉堡、薯条、炸鸡等西式快餐',
          location: '学生活动中心',
          opening_hours: '10:00-22:30',
          dish_count: 28,
          rating: 4.3,
          is_open: true,
          specialty: '汉堡炸鸡',
          average_price: 20,
          opening_days: [1, 2, 3, 4, 5, 6, 7],
          ingredients: ['鸡肉', '牛肉', '面包', '蔬菜', '薯条']
        },
        {
          id: 5,
          name: '素食餐厅',
          description: '健康素食，营养均衡，适合素食爱好者',
          location: '学生食堂三楼',
          opening_hours: '07:30-21:00',
          dish_count: 32,
          rating: 4.7,
          is_open: true,
          specialty: '健康素食',
          average_price: 16,
          opening_days: [1, 2, 3, 4, 5],
          ingredients: ['蔬菜', '水果', '豆类', '米饭', '面条']
        },
        {
          id: 6,
          name: '奶茶店',
          description: '各类奶茶、果茶、甜品，休闲好去处',
          location: '商业街',
          opening_hours: '09:00-23:00',
          dish_count: 45,
          rating: 4.4,
          is_open: true,
          specialty: '奶茶甜品',
          average_price: 12,
          opening_days: [1, 2, 3, 4, 5, 6, 7],
          ingredients: ['牛奶', '茶叶', '水果', '糖', '珍珠']
        },
        {
          id: 7,
          name: '特色小吃街',
          description: '各种地方特色小吃，品种丰富',
          location: '商业街',
          opening_hours: '11:00-22:00',
          dish_count: 68,
          rating: 4.6,
          is_open: true,
          specialty: '地方小吃',
          average_price: 10,
          opening_days: [6, 7],
          ingredients: ['各种小吃', '地方特色', '快餐']
        }
      ],
      // 今日推荐菜品
      todayRecommendations: [
        {
          id: 1,
          dish_name: '宫保鸡丁',
          restaurant_id: 1,
          restaurant_name: '学生餐厅',
          price: 12,
          rating: 4.5,
          monthly_sales: 1250
        },
        {
          id: 2,
          dish_name: '牛肉拉面',
          restaurant_id: 3,
          restaurant_name: '清真餐厅',
          price: 15,
          rating: 4.8,
          monthly_sales: 980
        },
        {
          id: 3,
          dish_name: '芝士汉堡',
          restaurant_id: 4,
          restaurant_name: '西式快餐',
          price: 18,
          rating: 4.3,
          monthly_sales: 890
        },
        {
          id: 4,
          dish_name: '蔬菜沙拉',
          restaurant_id: 5,
          restaurant_name: '素食餐厅',
          price: 16,
          rating: 4.7,
          monthly_sales: 750
        }
      ],
      // 性价比推荐菜品
      costEffectiveRecommendations: [
        {
          id: 5,
          dish_name: '番茄炒蛋',
          restaurant_id: 1,
          restaurant_name: '学生餐厅',
          price: 8,
          rating: 4.4,
          monthly_sales: 1560,
          cost_effective_score: 9.5
        },
        {
          id: 6,
          dish_name: '香辣鸡腿堡',
          restaurant_id: 4,
          restaurant_name: '西式快餐',
          price: 15,
          rating: 4.2,
          monthly_sales: 1120,
          cost_effective_score: 9.2
        },
        {
          id: 7,
          dish_name: '杂粮煎饼',
          restaurant_id: 1,
          restaurant_name: '学生餐厅',
          price: 6,
          rating: 4.3,
          monthly_sales: 2030,
          cost_effective_score: 9.8
        },
        {
          id: 8,
          dish_name: '原味奶茶',
          restaurant_id: 6,
          restaurant_name: '奶茶店',
          price: 10,
          rating: 4.5,
          monthly_sales: 1890,
          cost_effective_score: 9.3
        }
      ]
    }
  },
  computed: {
    // 获取当前星期几（1-7，周一到周日）
    currentDay() {
      const day = new Date().getDay()
      return day === 0 ? 7 : day
    },
    
    // 过滤当前开放的餐厅
    openRestaurants() {
      return this.restaurants.filter(restaurant => {
        // 检查是否在开放日期内
        return restaurant.opening_days.includes(this.currentDay)
      })
    },
    
    filteredRestaurants() {
      let restaurants = [...this.openRestaurants]
      
      // 搜索过滤
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        restaurants = restaurants.filter(restaurant => {
          // 餐厅名称或地址搜索
          const nameMatch = restaurant.name.toLowerCase().includes(query)
          const locationMatch = restaurant.location.toLowerCase().includes(query)
          const specialtyMatch = restaurant.specialty.toLowerCase().includes(query)
          // 新增食材搜索
          const ingredientMatch = restaurant.ingredients.some(ingredient => 
            ingredient.toLowerCase().includes(query)
          )
          
          return nameMatch || locationMatch || specialtyMatch || ingredientMatch
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
        case 'price_asc':
          restaurants.sort((a, b) => a.average_price - b.average_price)
          break
        case 'price_desc':
          restaurants.sort((a, b) => b.average_price - a.average_price)
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
    },
    // 根据当前星期几生成不同的推荐内容
    generateDailyRecommendations() {
      // 根据当前星期几生成不同的推荐内容
      const day = this.currentDay
      
      // 不同日期的推荐菜品
      const dailyDishes = {
        1: [ // 周一
          {
            id: 1,
            dish_name: '宫保鸡丁',
            restaurant_id: 1,
            restaurant_name: '学生餐厅',
            price: 12,
            rating: 4.5,
            monthly_sales: 1250
          },
          {
            id: 2,
            dish_name: '牛肉拉面',
            restaurant_id: 3,
            restaurant_name: '清真餐厅',
            price: 15,
            rating: 4.8,
            monthly_sales: 980
          },
          {
            id: 3,
            dish_name: '芝士汉堡',
            restaurant_id: 4,
            restaurant_name: '西式快餐',
            price: 18,
            rating: 4.3,
            monthly_sales: 890
          },
          {
            id: 4,
            dish_name: '蔬菜沙拉',
            restaurant_id: 5,
            restaurant_name: '素食餐厅',
            price: 16,
            rating: 4.7,
            monthly_sales: 750
          }
        ],
        2: [ // 周二
          {
            id: 5,
            dish_name: '红烧肉',
            restaurant_id: 1,
            restaurant_name: '学生餐厅',
            price: 15,
            rating: 4.6,
            monthly_sales: 1120
          },
          {
            id: 6,
            dish_name: '大盘鸡',
            restaurant_id: 3,
            restaurant_name: '清真餐厅',
            price: 20,
            rating: 4.9,
            monthly_sales: 850
          },
          {
            id: 7,
            dish_name: '炸鸡套餐',
            restaurant_id: 4,
            restaurant_name: '西式快餐',
            price: 25,
            rating: 4.4,
            monthly_sales: 780
          },
          {
            id: 8,
            dish_name: '番茄鸡蛋面',
            restaurant_id: 5,
            restaurant_name: '素食餐厅',
            price: 12,
            rating: 4.5,
            monthly_sales: 920
          }
        ],
        3: [ // 周三
          {
            id: 9,
            dish_name: '鱼香肉丝',
            restaurant_id: 1,
            restaurant_name: '学生餐厅',
            price: 13,
            rating: 4.7,
            monthly_sales: 1050
          },
          {
            id: 10,
            dish_name: '手抓饭',
            restaurant_id: 3,
            restaurant_name: '清真餐厅',
            price: 18,
            rating: 4.8,
            monthly_sales: 890
          },
          {
            id: 11,
            dish_name: '披萨',
            restaurant_id: 4,
            restaurant_name: '西式快餐',
            price: 30,
            rating: 4.5,
            monthly_sales: 650
          },
          {
            id: 12,
            dish_name: '蔬菜炒饭',
            restaurant_id: 5,
            restaurant_name: '素食餐厅',
            price: 14,
            rating: 4.6,
            monthly_sales: 820
          }
        ],
        4: [ // 周四
          {
            id: 13,
            dish_name: '糖醋排骨',
            restaurant_id: 1,
            restaurant_name: '学生餐厅',
            price: 16,
            rating: 4.8,
            monthly_sales: 980
          },
          {
            id: 14,
            dish_name: '烤羊腿',
            restaurant_id: 3,
            restaurant_name: '清真餐厅',
            price: 35,
            rating: 4.9,
            monthly_sales: 520
          },
          {
            id: 15,
            dish_name: '热狗套餐',
            restaurant_id: 4,
            restaurant_name: '西式快餐',
            price: 22,
            rating: 4.3,
            monthly_sales: 750
          },
          {
            id: 16,
            dish_name: '豆腐汤',
            restaurant_id: 5,
            restaurant_name: '素食餐厅',
            price: 10,
            rating: 4.4,
            monthly_sales: 1050
          }
        ],
        5: [ // 周五
          {
            id: 17,
            dish_name: '麻婆豆腐',
            restaurant_id: 1,
            restaurant_name: '学生餐厅',
            price: 11,
            rating: 4.6,
            monthly_sales: 1280
          },
          {
            id: 18,
            dish_name: '烤羊肉串',
            restaurant_id: 3,
            restaurant_name: '清真餐厅',
            price: 20,
            rating: 4.8,
            monthly_sales: 790
          },
          {
            id: 19,
            dish_name: '牛排',
            restaurant_id: 4,
            restaurant_name: '西式快餐',
            price: 45,
            rating: 4.7,
            monthly_sales: 480
          },
          {
            id: 20,
            dish_name: '水果沙拉',
            restaurant_id: 5,
            restaurant_name: '素食餐厅',
            price: 18,
            rating: 4.5,
            monthly_sales: 690
          }
        ],
        6: [ // 周六
          {
            id: 21,
            dish_name: '周末特惠套餐',
            restaurant_id: 1,
            restaurant_name: '学生餐厅',
            price: 25,
            rating: 4.7,
            monthly_sales: 850
          },
          {
            id: 22,
            dish_name: '烤全羊',
            restaurant_id: 3,
            restaurant_name: '清真餐厅',
            price: 128,
            rating: 4.9,
            monthly_sales: 230
          },
          {
            id: 23,
            dish_name: '家庭套餐',
            restaurant_id: 4,
            restaurant_name: '西式快餐',
            price: 68,
            rating: 4.6,
            monthly_sales: 320
          },
          {
            id: 24,
            dish_name: '素食火锅',
            restaurant_id: 5,
            restaurant_name: '素食餐厅',
            price: 38,
            rating: 4.8,
            monthly_sales: 450
          },
          {
            id: 25,
            dish_name: '特色小吃拼盘',
            restaurant_id: 7,
            restaurant_name: '特色小吃街',
            price: 28,
            rating: 4.7,
            monthly_sales: 680
          }
        ],
        7: [ // 周日
          {
            id: 26,
            dish_name: '周日早餐套餐',
            restaurant_id: 1,
            restaurant_name: '学生餐厅',
            price: 12,
            rating: 4.5,
            monthly_sales: 720
          },
          {
            id: 27,
            dish_name: '羊肉汤',
            restaurant_id: 3,
            restaurant_name: '清真餐厅',
            price: 22,
            rating: 4.8,
            monthly_sales: 650
          },
          {
            id: 28,
            dish_name: '周日特价披萨',
            restaurant_id: 4,
            restaurant_name: '西式快餐',
            price: 25,
            rating: 4.4,
            monthly_sales: 580
          },
          {
            id: 29,
            dish_name: '周日素食特惠',
            restaurant_id: 5,
            restaurant_name: '素食餐厅',
            price: 15,
            rating: 4.6,
            monthly_sales: 620
          },
          {
            id: 30,
            dish_name: '小吃街招牌套餐',
            restaurant_id: 7,
            restaurant_name: '特色小吃街',
            price: 35,
            rating: 4.8,
            monthly_sales: 780
          }
        ]
      }
      
      // 根据当前星期几更新推荐内容
      this.todayRecommendations = dailyDishes[day] || dailyDishes[1]
      
      // 生成性价比推荐（基于价格和评分的综合计算）
      this.generateCostEffectiveRecommendations()
    },
    
    // 生成性价比推荐
    generateCostEffectiveRecommendations() {
      // 从所有推荐中筛选出性价比最高的菜品
      const allDishes = [...this.todayRecommendations]
      
      // 计算性价比得分 = 评分 * 0.7 + (1 / 价格) * 30 * 0.3
      const dishesWithScore = allDishes.map(dish => {
        const costEffectiveScore = (dish.rating * 0.7 + (1 / dish.price) * 30 * 0.3).toFixed(1)
        return {
          ...dish,
          cost_effective_score: parseFloat(costEffectiveScore)
        }
      })
      
      // 按性价比得分排序，取前4个
      this.costEffectiveRecommendations = dishesWithScore
        .sort((a, b) => b.cost_effective_score - a.cost_effective_score)
        .slice(0, 4)
    }
  },
  
  // 组件创建时生成推荐内容
  created() {
    this.generateDailyRecommendations()
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

.fade-enter, .fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* 推荐区域样式 */
.recommendation-section {
  margin: 20px 0;
}

.section-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 16px;
  color: #333;
}

.mt-20 {
  margin-top: 20px;
}

.recommendation-card {
  margin-bottom: 20px;
  border-radius: 8px;
}

.recommendation-content {
  display: flex;
  gap: 20px;
  overflow-x: auto;
  padding: 10px 0;
  scrollbar-width: thin;
}

.recommendation-item {
  display: flex;
  width: 300px;
  min-width: 300px;
  gap: 12px;
  padding: 10px;
  background: #fafafa;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.recommendation-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.recommendation-image {
  width: 100px;
  height: 100px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 18px;
  flex-shrink: 0;
}

.recommendation-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.recommendation-info h4 {
  margin: 0;
  font-size: 16px;
  font-weight: bold;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
}

.recommendation-info .restaurant-name {
  margin: 0;
  font-size: 14px;
  color: #666;
}

.recommendation-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  margin: 8px 0;
}

.recommendation-meta .price {
  font-weight: bold;
  color: #f56c6c;
}

.recommendation-meta .rating {
  display: flex;
  align-items: center;
  gap: 4px;
}

.recommendation-meta .sales, .recommendation-meta .cost-effective {
  color: #909399;
  font-size: 12px;
}

.recommendation-item .el-button {
  margin-top: auto;
  width: 100px;
}

/* 深色模式样式 */
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

:deep(.dark-mode) .section-title {
  color: #e0e0e0;
}

:deep(.dark-mode) .recommendation-item {
  background: #333;
}

:deep(.dark-mode) .recommendation-info h4 {
  color: #e0e0e0;
}

:deep(.dark-mode) .recommendation-info .restaurant-name {
  color: #999;
}

:deep(.dark-mode) .recommendation-meta .sales, :deep(.dark-mode) .recommendation-meta .cost-effective {
  color: #777;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .restaurants-wrapper {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 16px;
  }
  
  .recommendation-item {
    width: 250px;
    min-width: 250px;
  }
  
  .filter-bar {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-input, .sort-select {
    width: 100%;
    margin-bottom: 12px;
  }
}
</style>
