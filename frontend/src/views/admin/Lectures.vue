<template>
  <div class="admin-lectures">
    <el-card shadow="hover">
      <div slot="header" class="clearfix">
        <span>讲座管理</span>
        <el-button type="primary" icon="el-icon-plus" class="button-new-tag" @click="addLecture">
          添加讲座
        </el-button>
      </div>
      <el-table :data="lectures" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="title" label="讲座标题"></el-table-column>
        <el-table-column prop="speaker" label="主讲人"></el-table-column>
        <el-table-column prop="location" label="地点"></el-table-column>
        <el-table-column prop="lecture_date" label="讲座日期"></el-table-column>
        <el-table-column prop="start_time" label="开始时间"></el-table-column>
        <el-table-column prop="end_time" label="结束时间"></el-table-column>
        <el-table-column label="操作" width="200">
          <template slot-scope="scope">
            <el-button type="primary" size="small" @click="editLecture(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="deleteLecture(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'AdminLectures',
  data() {
    return {
      lectures: []
    }
  },
  created() {
    this.fetchLectures()
  },
  methods: {
    fetchLectures() {
      // 调用API获取讲座列表
      this.$axios.get('/timetable/lectures/')
        .then(response => {
          this.lectures = response.data.results
          console.log('获取讲座列表成功:', this.lectures)
        })
        .catch(error => {
          console.error('获取讲座列表失败:', error)
          this.$message.error('获取讲座列表失败')
        })
    },
    addLecture() {
      console.log('添加讲座')
    },
    editLecture(lecture) {
      console.log('编辑讲座:', lecture)
    },
    deleteLecture(lecture) {
      console.log('删除讲座:', lecture)
    }
  }
}
</script>

<style scoped>
.admin-lectures {
  padding: 20px;
}

.button-new-tag {
  float: right;
  margin-bottom: 10px;
}
</style>