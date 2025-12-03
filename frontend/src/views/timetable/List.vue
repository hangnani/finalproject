<template>
  <div class="timetable-container">
    <div class="timetable-header">
      <h2>课程表</h2>
      <div class="header-actions">
        <el-button type="primary" @click="$router.push('/timetable/add')">添加课程</el-button>
        <el-button @click="$router.push('/timetable/import')">导入课程</el-button>
        <el-select v-model="currentWeek" placeholder="选择周数" style="width: 120px; margin-left: 10px;">
          <el-option v-for="week in 20" :key="week" :label="`第${week}周`" :value="week"></el-option>
        </el-select>
      </div>
    </div>
    
    <div class="timetable-content">
      <div class="timetable-grid">
        <!-- 时间轴 -->
        <div class="time-axis">
          <div v-for="time in timeSlots" :key="time.id" class="time-slot">
            {{ time.text }}
          </div>
        </div>
        
        <!-- 课程表主体 -->
        <div class="timetable-main">
          <!-- 星期标题 -->
          <div class="week-header">
            <div v-for="day in weekDays" :key="day.id" class="week-day">
              {{ day.name }}
            </div>
          </div>
          
          <!-- 课程格子 -->
          <div class="timetable-body">
            <div v-for="day in weekDays" :key="day.id" class="day-column">
              <div v-for="time in timeSlots" :key="time.id" class="course-cell">
                <!-- 这里应该根据day.id和time.id渲染对应的课程 -->
                <div v-for="course in getCoursesByDayAndTime(day.id, time.id)" :key="course.id" class="course-item" :style="{ backgroundColor: getRandomColor(course.id) }">
                  <div class="course-name">{{ course.name }}</div>
                  <div class="course-info">{{ course.teacher }} | {{ course.location }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 课程列表 -->
    <div class="courses-list">
      <h3>本周课程列表</h3>
      <el-table :data="courses" style="width: 100%">
        <el-table-column prop="name" label="课程名称" width="200"></el-table-column>
        <el-table-column prop="teacher" label="教师" width="150"></el-table-column>
        <el-table-column prop="day_of_week" label="星期" width="100">
          <template slot-scope="scope">
            {{ getDayName(scope.row.day_of_week) }}
          </template>
        </el-table-column>
        <el-table-column prop="start_time" label="开始时间" width="120"></el-table-column>
        <el-table-column prop="end_time" label="结束时间" width="120"></el-table-column>
        <el-table-column prop="location" label="地点" width="150"></el-table-column>
        <el-table-column prop="credit" label="学分" width="80"></el-table-column>
        <el-table-column label="操作" width="150">
          <template slot-scope="scope">
            <el-button size="small" @click="editCourse(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteCourse(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TimetableList',
  data() {
    return {
      currentWeek: 1,
      weekDays: [
        { id: 1, name: '周一' },
        { id: 2, name: '周二' },
        { id: 3, name: '周三' },
        { id: 4, name: '周四' },
        { id: 5, name: '周五' },
        { id: 6, name: '周六' },
        { id: 7, name: '周日' }
      ],
      timeSlots: [
        { id: 1, text: '08:00-09:40' },
        { id: 2, text: '10:00-11:40' },
        { id: 3, text: '14:00-15:40' },
        { id: 4, text: '16:00-17:40' },
        { id: 5, text: '19:00-20:40' }
      ],
      courses: [
        // 这里是模拟数据，实际应该从API获取
        {
          id: 1,
          name: '高等数学',
          teacher: '张老师',
          day_of_week: 1,
          start_time: '08:00',
          end_time: '09:40',
          location: '教1-101',
          credit: 4
        },
        {
          id: 2,
          name: '大学英语',
          teacher: '李老师',
          day_of_week: 2,
          start_time: '10:00',
          end_time: '11:40',
          location: '教2-203',
          credit: 3
        },
        {
          id: 3,
          name: '计算机导论',
          teacher: '王老师',
          day_of_week: 3,
          start_time: '14:00',
          end_time: '15:40',
          location: '实验楼-305',
          credit: 2
        }
      ]
    }
  },
  methods: {
    getCoursesByDayAndTime(dayId, timeId) {
      // 这里应该根据dayId和timeId过滤课程
      return this.courses.filter(course => course.day_of_week === dayId);
    },
    getDayName(dayId) {
      const day = this.weekDays.find(d => d.id === dayId);
      return day ? day.name : '';
    },
    getRandomColor(id) {
      // 生成随机颜色，用于区分不同课程
      const colors = ['#FFB6C1', '#87CEFA', '#98FB98', '#F0E68C', '#DDA0DD', '#FFA07A'];
      return colors[id % colors.length];
    },
    editCourse(course) {
      // 编辑课程逻辑
      this.$router.push({ path: '/timetable/add', query: { id: course.id } });
    },
    deleteCourse(course) {
      // 删除课程逻辑
      this.$confirm('确定要删除这门课程吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 这里应该调用删除课程的API
        this.courses = this.courses.filter(c => c.id !== course.id);
        this.$message.success('课程删除成功');
      }).catch(() => {
        this.$message.info('已取消删除');
      });
    }
  }
}
</script>

<style scoped>
.timetable-container {
  padding: 20px;
}

.timetable-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-actions {
  display: flex;
  align-items: center;
}

.timetable-content {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.timetable-grid {
  display: flex;
}

.time-axis {
  width: 80px;
  margin-right: 10px;
}

.time-slot {
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: #666;
  border-bottom: 1px solid #eee;
}

.timetable-main {
  flex: 1;
}

.week-header {
  display: flex;
  margin-bottom: 10px;
}

.week-day {
  flex: 1;
  text-align: center;
  font-weight: bold;
  padding: 10px 0;
  background: #f5f7fa;
  border-radius: 4px;
  margin-right: 10px;
}

.timetable-body {
  display: flex;
}

.day-column {
  flex: 1;
  margin-right: 10px;
}

.course-cell {
  height: 100px;
  border: 1px solid #eee;
  border-radius: 4px;
  margin-bottom: 10px;
  padding: 5px;
  position: relative;
  overflow: hidden;
}

.course-item {
  background: #409EFF;
  color: #fff;
  padding: 5px;
  border-radius: 4px;
  font-size: 12px;
  margin-bottom: 5px;
  cursor: pointer;
  transition: all 0.3s;
}

.course-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.course-name {
  font-weight: bold;
  margin-bottom: 3px;
}

.course-info {
  font-size: 10px;
  opacity: 0.9;
}

.courses-list {
  margin-top: 30px;
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
</style>