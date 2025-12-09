<template>
  <div class="admin-users">
    <el-card shadow="hover">
      <div slot="header" class="clearfix">
        <span>用户管理</span>
      </div>
      <el-table :data="users" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="username" label="用户名"></el-table-column>
        <el-table-column prop="email" label="邮箱"></el-table-column>
        <el-table-column prop="name" label="姓名"></el-table-column>
        <el-table-column prop="student_id" label="学号"></el-table-column>
        <el-table-column prop="phone" label="手机号"></el-table-column>
        <el-table-column prop="is_admin" label="是否管理员" width="120">
          <template slot-scope="scope">
            <el-switch v-model="scope.row.is_admin" @change="updateUserRole(scope.row)"></el-switch>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template slot-scope="scope">
            <el-button type="primary" size="small" @click="editUser(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="deleteUser(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'AdminUsers',
  data() {
    return {
      users: []
    }
  },
  created() {
    this.fetchUsers()
  },
  methods: {
    fetchUsers() {
      // 调用API获取用户列表
      this.$axios.get('/users/users/')
        .then(response => {
          this.users = response.data.results || response.data
          console.log('获取用户列表成功:', this.users)
        })
        .catch(error => {
          console.error('获取用户列表失败:', error)
          this.$message.error('获取用户列表失败')
        })
    },
    updateUserRole(user) {
      console.log('更新用户角色:', user)
    },
    editUser(user) {
      console.log('编辑用户:', user)
    },
    deleteUser(user) {
      console.log('删除用户:', user)
    }
  }
}
</script>

<style scoped>
.admin-users {
  padding: 20px;
}
</style>