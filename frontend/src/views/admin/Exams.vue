<template>
  <div class="admin-exams">
    <el-card shadow="hover">
      <div slot="header" class="clearfix">
        <span>考试管理</span>
        <el-button type="primary" icon="el-icon-plus" class="button-new-tag" @click="addExam">
          添加考试
        </el-button>
      </div>
      <el-table :data="exams" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="name" label="考试名称"></el-table-column>
        <el-table-column prop="course.name" label="课程名称"></el-table-column>
        <el-table-column prop="exam_date" label="考试日期"></el-table-column>
        <el-table-column prop="start_time" label="开始时间"></el-table-column>
        <el-table-column prop="end_time" label="结束时间"></el-table-column>
        <el-table-column prop="location" label="考试地点"></el-table-column>
        <el-table-column label="操作" width="200">
          <template slot-scope="scope">
            <el-button type="primary" size="small" @click="editExam(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="deleteExam(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'AdminExams',
  data() {
    return {
      exams: []
    }
  },
  created() {
    this.fetchExams()
  },
  methods: {
    fetchExams() {
      // 调用API获取考试列表
      this.$axios.get('/timetable/exams/')
        .then(response => {
          this.exams = response.data.results
          console.log('获取考试列表成功:', this.exams)
        })
        .catch(error => {
          console.error('获取考试列表失败:', error)
          this.$message.error('获取考试列表失败')
        })
    },
    addExam() {
      console.log('添加考试')
    },
    editExam(exam) {
      console.log('编辑考试:', exam)
    },
    deleteExam(exam) {
      console.log('删除考试:', exam)
    }
  }
}
</script>

<style scoped>
.admin-exams {
  padding: 20px;
}

.button-new-tag {
  float: right;
  margin-bottom: 10px;
}
</style>