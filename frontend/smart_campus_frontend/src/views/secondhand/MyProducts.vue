<template>
  <div class="secondhand-my-products-container">
    <h2>我的发布</h2>
    <el-card>
      <el-table :data="myProducts" style="width: 100%">
        <el-table-column prop="name" label="商品名称" min-width="200"></el-table-column>
        <el-table-column prop="price" label="价格" width="100" formatter="formatPrice"></el-table-column>
        <el-table-column prop="status" label="状态" width="100" formatter="formatStatus"></el-table-column>
        <el-table-column prop="created_at" label="发布时间" width="180" formatter="formatTime"></el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template slot-scope="scope">
            <el-button type="primary" size="small" @click="viewDetail(scope.row.id)">查看</el-button>
            <el-button type="warning" size="small" @click="editProduct(scope.row.id)">编辑</el-button>
            <el-button type="danger" size="small" @click="deleteProduct(scope.row.id)">删除</el-button>
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
  name: 'SecondhandMyProducts',
  data() {
    return {
      myProducts: [],
      currentPage: 1,
      pageSize: 10,
      totalProducts: 0
    }
  },
  created() {
    this.getMyProducts()
  },
  methods: {
    getMyProducts() {
      // 这里应该调用 API 获取用户发布的商品列表
      // 暂时使用模拟数据
      this.myProducts = [
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
        }
      ]
      this.totalProducts = this.myProducts.length
    },
    viewDetail(productId) {
      this.$router.push(`/secondhand/detail/${productId}`)
    },
    editProduct(productId) {
      // 编辑商品逻辑
      this.$message.info('编辑功能开发中...')
    },
    deleteProduct(productId) {
      this.$confirm('确定要删除这个商品吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 删除商品逻辑
        this.$message.success('商品删除成功！')
        this.getMyProducts()
      }).catch(() => {
        this.$message.info('已取消删除')
      })
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.currentPage = 1
      this.getMyProducts()
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.getMyProducts()
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
.secondhand-my-products-container {
  padding: 0;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>