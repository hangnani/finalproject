<template>
  <div class="foodorder-cart-container">
    <h2>购物车</h2>
    
    <div v-if="cartItems.length === 0" class="empty-cart">
      <el-empty description="购物车是空的"></el-empty>
      <el-button type="primary" @click="$router.push('/foodorder/restaurants')">去点餐</el-button>
    </div>
    
    <div v-else class="cart-content">
      <el-table :data="cartItems" style="width: 100%" border>
        <el-table-column prop="dish.name" label="菜品名称" width="200"></el-table-column>
        <el-table-column prop="dish.price" label="单价" width="100">
          <template slot-scope="scope">¥{{ scope.row.dish.price.toFixed(2) }}</template>
        </el-table-column>
        <el-table-column label="数量" width="150">
          <template slot-scope="scope">
            <el-input-number
              v-model="scope.row.quantity"
              :min="1"
              :max="10"
              @change="updateQuantity(scope.row)"
            ></el-input-number>
          </template>
        </el-table-column>
        <el-table-column label="小计" width="100">
          <template slot-scope="scope">¥{{ (scope.row.dish.price * scope.row.quantity).toFixed(2) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="100">
          <template slot-scope="scope">
            <el-button type="danger" size="small" @click="removeFromCart(scope.row.id)">
              <i class="el-icon-delete"></i> 删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="cart-footer">
        <div class="cart-total">
          <span>总计：</span>
          <span class="total-price">¥{{ totalPrice.toFixed(2) }}</span>
        </div>
        <div class="cart-actions">
          <el-button @click="clearCart">清空购物车</el-button>
          <el-button type="primary" @click="goToCheckout">去结算</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FoodorderCart',
  data() {
    return {
      cartItems: [
        // 模拟数据
        {
          id: 1,
          dish: {
            id: 1,
            name: '宫保鸡丁',
            price: 18.00
          },
          quantity: 2
        },
        {
          id: 2,
          dish: {
            id: 2,
            name: '鱼香肉丝',
            price: 16.00
          },
          quantity: 1
        }
      ]
    }
  },
  computed: {
    totalPrice() {
      return this.cartItems.reduce((total, item) => {
        return total + (item.dish.price * item.quantity)
      }, 0)
    }
  },
  methods: {
    updateQuantity(item) {
      // 这里应该调用API更新购物车数量
      this.$message.success('购物车已更新')
    },
    removeFromCart(id) {
      // 这里应该调用API删除购物车项
      this.cartItems = this.cartItems.filter(item => item.id !== id)
      this.$message.success('已从购物车中删除')
    },
    clearCart() {
      this.$confirm('确定要清空购物车吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 这里应该调用API清空购物车
        this.cartItems = []
        this.$message.success('购物车已清空')
      }).catch(() => {
        this.$message.info('已取消清空')
      })
    },
    goToCheckout() {
      // 这里应该跳转到结算页面，目前直接跳转到订单列表
      this.$message.success('订单已提交')
      this.$router.push('/foodorder/orders')
    }
  }
}
</script>

<style scoped>
.foodorder-cart-container {
  padding: 20px;
}

.empty-cart {
  text-align: center;
  margin: 50px 0;
}

.cart-content {
  max-width: 800px;
}

.cart-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 4px;
}

.cart-total {
  font-size: 18px;
  font-weight: bold;
}

.total-price {
  color: #f56c6c;
  font-size: 24px;
  margin-left: 10px;
}

.cart-actions {
  display: flex;
  gap: 10px;
}
</style>