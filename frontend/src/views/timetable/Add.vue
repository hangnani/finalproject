<template>
  <div class="timetable-add-container">
    <h2>{{ isEdit ? '编辑课程' : '添加课程' }}</h2>
    <el-form :model="courseForm" :rules="courseRules" ref="courseForm" label-width="120px" class="course-form">
      <el-form-item label="课程名称" prop="name">
        <el-input v-model="courseForm.name" placeholder="请输入课程名称"></el-input>
      </el-form-item>
      <el-form-item label="教师姓名" prop="teacher">
        <el-input v-model="courseForm.teacher" placeholder="请输入教师姓名"></el-input>
      </el-form-item>
      <el-form-item label="星期几" prop="day_of_week">
        <el-select v-model="courseForm.day_of_week" placeholder="请选择星期几">
          <el-option label="周一" :value="1"></el-option>
          <el-option label="周二" :value="2"></el-option>
          <el-option label="周三" :value="3"></el-option>
          <el-option label="周四" :value="4"></el-option>
          <el-option label="周五" :value="5"></el-option>
          <el-option label="周六" :value="6"></el-option>
          <el-option label="周日" :value="7"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="开始时间" prop="start_time">
        <el-time-picker v-model="courseForm.start_time" placeholder="选择开始时间" format="HH:mm" value-format="HH:mm"></el-time-picker>
      </el-form-item>
      <el-form-item label="结束时间" prop="end_time">
        <el-time-picker v-model="courseForm.end_time" placeholder="选择结束时间" format="HH:mm" value-format="HH:mm"></el-time-picker>
      </el-form-item>
      <el-form-item label="上课地点" prop="location">
        <el-input v-model="courseForm.location" placeholder="请输入上课地点"></el-input>
      </el-form-item>
      <el-form-item label="学分" prop="credit">
        <el-input-number v-model="courseForm.credit" :min="0.5" :max="10" :step="0.5" placeholder="请输入学分"></el-input-number>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm">提交</el-button>
        <el-button @click="resetForm">重置</el-button>
        <el-button @click="$router.go(-1)">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: 'TimetableAdd',
  data() {
    return {
      isEdit: false,
      courseId: null,
      courseForm: {
        name: '',
        teacher: '',
        day_of_week: '',
        start_time: '',
        end_time: '',
        location: '',
        credit: 2
      },
      courseRules: {
        name: [
          { required: true, message: '请输入课程名称', trigger: 'blur' },
          { min: 2, max: 50, message: '课程名称长度在 2 到 50 个字符', trigger: 'blur' }
        ],
        teacher: [
          { required: true, message: '请输入教师姓名', trigger: 'blur' },
          { min: 1, max: 20, message: '教师姓名长度在 1 到 20 个字符', trigger: 'blur' }
        ],
        day_of_week: [
          { required: true, message: '请选择星期几', trigger: 'change' }
        ],
        start_time: [
          { required: true, message: '请选择开始时间', trigger: 'change' }
        ],
        end_time: [
          { required: true, message: '请选择结束时间', trigger: 'change' }
        ],
        location: [
          { required: true, message: '请输入上课地点', trigger: 'blur' },
          { min: 2, max: 50, message: '上课地点长度在 2 到 50 个字符', trigger: 'blur' }
        ],
        credit: [
          { required: true, message: '请输入学分', trigger: 'blur' }
        ]
      }
    }
  },
  mounted() {
    // 检查是否是编辑模式
    const id = this.$route.query.id
    if (id) {
      this.isEdit = true
      this.courseId = id
      this.getCourseDetail()
    }
  },
  methods: {
    getCourseDetail() {
      // 调用API获取课程详情
      this.$axios.get(`/timetable/courses/${this.courseId}/`)
        .then(response => {
          this.courseForm = response.data;
        })
        .catch(error => {
          console.error('获取课程详情失败:', error);
          this.$message.error('获取课程详情失败，请稍后重试');
          this.$router.go(-1);
        });
    },
    submitForm() {
      this.$refs.courseForm.validate((valid) => {
        if (valid) {
          // 调用API保存课程
          if (this.isEdit) {
            // 编辑课程
            this.$axios.put(`/timetable/courses/${this.courseId}/`, this.courseForm)
              .then(response => {
                this.$message.success('课程编辑成功')
                this.$router.push('/timetable')
              })
              .catch(error => {
                console.error('编辑课程失败:', error)
                console.error('错误详情:', error.response)
                this.$message.error(`编辑课程失败: ${error.response?.data?.message || '请稍后重试'}`)
              })
          } else {
            // 添加课程
            this.$axios.post('/timetable/courses/', this.courseForm)
              .then(response => {
                this.$message.success('课程添加成功')
                this.$router.push('/timetable')
              })
              .catch(error => {
                console.error('添加课程失败:', error)
                console.error('错误详情:', error.response)
                this.$message.error(`添加课程失败: ${error.response?.data?.message || '请稍后重试'}`)
              })
          }
        } else {
          return false
        }
      })
    },
    resetForm() {
      this.$refs.courseForm.resetFields()
    }
  }
}
</script>

<style scoped>
.timetable-add-container {
  padding: 20px;
}

.course-form {
  max-width: 600px;
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
</style>