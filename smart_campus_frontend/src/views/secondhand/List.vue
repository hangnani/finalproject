<template>
  <div class="secondhand-list-container">
    <h2>二手交易</h2>
    <el-card>
      <div class="filter-bar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索商品"
          prefix-icon="el-icon-search"
          class="search-input"
        ></el-input>
        <el-button type="primary" @click="handleSearch">搜索</el-button>
      </div>
      
      <el-table :data="products" style="width: 100%">
        <el-table-column prop="name" label="商品名称" min-width="200"></el-table-column>
        <el-table-column prop="price" label="价格" width="100" formatter="formatPrice"></el-table-column>
        <el-table-column prop="status" label="状态" width="100" formatter="formatStatus"></el-table-column>
        <el-table-column prop="created_at" label="发布时间" width="180" formatter="formatTime"></el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template slot-scope="scope">
            <el-button type="primary" size="small" @click="viewDetail(scope.row.id)">查看</el-button>
            <el-button type="success" size="small" @click="addToFavorite(scope.row.id)">收藏</el-button>
          </template>
        </el-table-column>
      </el-table>
      
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
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'SecondhandList',
  data() {
    return {
      searchQuery: '',
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
    getProducts() {
      // 这里应该调用 API 获取商品列表
      // 暂时使用模拟数据
      this.products = [
        {
          id: 1,
          name: '《Python编程从入门到精通》',
          price: 29.99,
          status: 0,
          created_at: '2025-11-27T10:30:00'
        },
        {
          id: 2,
          name: '无线鼠标',
          price: 19.99,
          status: 0,
          created_at: '2025-11-26T14:20:00'
        },
        {
          id: 3,
          name: '机械键盘',
          price: 89.99,
          status: 1,
          created_at: '2025-11-25T09:15:00'
        }
      ]
      this.totalProducts = this.products.length
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
    formatPrice(row, column, cellValue) {
      return `¥${cellValue}`
    },
    formatStatus(row, column, cellValue) {
      return cellValue === 0 ? '在售' : '已售出'
    },
    formatTime(row, column, cellValue) {
      return new Date(cellValue).toLocaleString()
    }
  }
}
</script>

<style scoped>
.secondhand-list-container {
  padding: 0;
}

.filter-bar {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
  align-items: center;
}

.search-input {
  width: 300px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>