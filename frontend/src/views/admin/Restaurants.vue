<template>
  <div class="admin-restaurants">
    <el-card shadow="hover">
      <div slot="header" class="clearfix">
        <span>餐厅管理</span>
        <el-button type="primary" icon="el-icon-plus" class="button-new-tag" @click="addRestaurant">
          添加餐厅
        </el-button>
      </div>
      <el-table :data="restaurants" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="name" label="餐厅名称"></el-table-column>
        <el-table-column prop="description" label="餐厅描述"></el-table-column>
        <el-table-column prop="location" label="地点"></el-table-column>
        <el-table-column prop="open_time" label="营业时间"></el-table-column>
        <el-table-column prop="close_time" label="打烊时间"></el-table-column>
        <el-table-column label="操作" width="200">
          <template slot-scope="scope">
            <el-button type="primary" size="small" @click="editRestaurant(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="deleteRestaurant(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'AdminRestaurants',
  data() {
    return {
      restaurants: []
    }
  },
  created() {
    this.fetchRestaurants()
  },
  methods: {
    fetchRestaurants() {
      // 调用API获取餐厅列表
      this.$axios.get('/foodorder/restaurants/')
        .then(response => {
          this.restaurants = response.data.results
          console.log('获取餐厅列表成功:', this.restaurants)
        })
        .catch(error => {
          console.error('获取餐厅列表失败:', error)
          this.$message.error('获取餐厅列表失败')
        })
    },
    addRestaurant() {
      console.log('添加餐厅')
    },
    editRestaurant(restaurant) {
      console.log('编辑餐厅:', restaurant)
    },
    deleteRestaurant(restaurant) {
      console.log('删除餐厅:', restaurant)
    }
  }
}
</script>

<style scoped>
.admin-restaurants {
  padding: 20px;
}

.button-new-tag {
  float: right;
  margin-bottom: 10px;
}
</style>