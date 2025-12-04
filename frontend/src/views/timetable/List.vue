<template>
  <div>
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
                <div 
                  v-for="course in getCoursesByDayAndTime(day.id, time.id)" 
                  :key="course.id" 
                  class="course-item" 
                  :style="{ backgroundColor: getRandomColor(course.id) }"
                  @click="showCourseDetailDialog(course)"
                >
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

    <!-- 课程详情对话框 -->
    <el-dialog
      title="课程详情"
      :visible.sync="showCourseDetail"
      width="500px"
    >
      <div v-if="currentCourse" class="course-detail-info">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="课程名称">{{ currentCourse.name }}</el-descriptions-item>
          <el-descriptions-item label="教师">{{ currentCourse.teacher }}</el-descriptions-item>
          <el-descriptions-item label="星期">{{ getDayName(currentCourse.day_of_week) }}</el-descriptions-item>
          <el-descriptions-item label="开始时间">{{ currentCourse.start_time }}</el-descriptions-item>
          <el-descriptions-item label="结束时间">{{ currentCourse.end_time }}</el-descriptions-item>
          <el-descriptions-item label="上课地点">{{ currentCourse.location }}</el-descriptions-item>
          <el-descriptions-item label="学分">{{ currentCourse.credit }}</el-descriptions-item>
        </el-descriptions>
      </div>
      <div v-else class="course-detail-empty">
        暂无课程详情
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showCourseDetail = false">关闭</el-button>
      </span>
    </el-dialog>
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
        { id: 1, text: '08:00-09:40', start: '08:00', end: '09:40' },
        { id: 2, text: '10:00-11:40', start: '10:00', end: '11:40' },
        { id: 3, text: '14:00-15:40', start: '14:00', end: '15:40' },
        { id: 4, text: '16:00-17:40', start: '16:00', end: '17:40' },
        { id: 5, text: '19:00-20:40', start: '19:00', end: '20:40' }
      ],
      // 课程详情对话框状态
      showCourseDetail: false,
      currentCourse: null,
      // 默认课程数据
      defaultCourses: [
        // 周一课程
        {
          id: 901,
          name: '高等数学',
          teacher: '张教授',
          day_of_week: 1,
          start_time: '08:00:00',
          end_time: '09:40:00',
          location: '教1-101',
          credit: 4
        },
        {
          id: 902,
          name: '大学英语',
          teacher: '李老师',
          day_of_week: 1,
          start_time: '10:00:00',
          end_time: '11:40:00',
          location: '教2-203',
          credit: 3
        },
        {
          id: 903,
          name: '计算机导论',
          teacher: '王讲师',
          day_of_week: 1,
          start_time: '14:00:00',
          end_time: '15:40:00',
          location: '实验楼-305',
          credit: 2
        },
        // 周二课程
        {
          id: 904,
          name: '线性代数',
          teacher: '刘教授',
          day_of_week: 2,
          start_time: '08:00:00',
          end_time: '09:40:00',
          location: '教1-102',
          credit: 3
        },
        {
          id: 905,
          name: '物理实验',
          teacher: '陈老师',
          day_of_week: 2,
          start_time: '14:00:00',
          end_time: '15:40:00',
          location: '物理实验楼-101',
          credit: 2
        },
        {
          id: 906,
          name: '中国近代史',
          teacher: '赵教授',
          day_of_week: 2,
          start_time: '16:00:00',
          end_time: '17:40:00',
          location: '教3-301',
          credit: 2
        },
        // 周三课程
        {
          id: 907,
          name: '概率论与数理统计',
          teacher: '孙教授',
          day_of_week: 3,
          start_time: '08:00:00',
          end_time: '09:40:00',
          location: '教1-103',
          credit: 3
        },
        {
          id: 908,
          name: '大学物理',
          teacher: '周老师',
          day_of_week: 3,
          start_time: '10:00:00',
          end_time: '11:40:00',
          location: '教2-205',
          credit: 4
        },
        {
          id: 909,
          name: '程序设计基础',
          teacher: '吴讲师',
          day_of_week: 3,
          start_time: '19:00:00',
          end_time: '20:40:00',
          location: '实验楼-401',
          credit: 3
        },
        // 周四课程
        {
          id: 910,
          name: '大学化学',
          teacher: '郑教授',
          day_of_week: 4,
          start_time: '08:00:00',
          end_time: '09:40:00',
          location: '教1-104',
          credit: 3
        },
        {
          id: 911,
          name: '数据结构',
          teacher: '冯老师',
          day_of_week: 4,
          start_time: '10:00:00',
          end_time: '11:40:00',
          location: '实验楼-303',
          credit: 3
        },
        {
          id: 912,
          name: '体育',
          teacher: '杨教练',
          day_of_week: 4,
          start_time: '14:00:00',
          end_time: '15:40:00',
          location: '操场',
          credit: 1
        },
        // 周五课程
        {
          id: 913,
          name: '操作系统',
          teacher: '朱教授',
          day_of_week: 5,
          start_time: '08:00:00',
          end_time: '09:40:00',
          location: '实验楼-403',
          credit: 3
        },
        {
          id: 914,
          name: '数据库原理',
          teacher: '郭老师',
          day_of_week: 5,
          start_time: '10:00:00',
          end_time: '11:40:00',
          location: '实验楼-405',
          credit: 3
        },
        {
          id: 915,
          name: '马克思主义原理',
          teacher: '黄教授',
          day_of_week: 5,
          start_time: '14:00:00',
          end_time: '15:40:00',
          location: '教3-305',
          credit: 2
        }
      ],
      courses: []
    }
  },
  mounted() {
    // 从API获取课程列表
    this.fetchCourses();
  },
  watch: {
    // 监听路由变化，当从添加课程页面返回时重新获取课程列表
    '$route': {
      handler() {
        this.fetchCourses();
      },
      immediate: false
    }
  },
  methods: {
    fetchCourses() {
      this.$axios.get('/timetable/courses/')
        .then(response => {
          console.log('获取到的课程数据:', response.data);
          // 检查API返回的数据结构，DRF可能返回包含results字段的对象
          const apiCourses = response.data.results || response.data;
          console.log('API返回的课程数据:', apiCourses);
          
          let finalCourses = [];
          
          // 如果API返回了课程数据
          if (Array.isArray(apiCourses)) {
            // 合并默认课程数据和API返回的数据
            // 创建一个Set来存储已存在的课程ID，避免重复
            const existingCourseIds = new Set(apiCourses.map(course => course.id));
            
            // 添加API返回的课程
            finalCourses = [...apiCourses];
            
            // 添加默认课程，排除已存在的课程ID
            this.defaultCourses.forEach(defaultCourse => {
              if (!existingCourseIds.has(defaultCourse.id)) {
                finalCourses.push(defaultCourse);
              }
            });
          } else {
            // 如果API返回的数据不是数组，则使用默认课程数据
            finalCourses = this.defaultCourses;
          }
          
          this.courses = finalCourses;
          console.log('最终课程列表:', this.courses);
        })
        .catch(error => {
          console.error('获取课程列表失败:', error);
          // 如果API请求失败，使用默认课程数据
          console.log('API请求失败，使用默认课程数据');
          this.courses = this.defaultCourses;
          // 不显示错误消息，避免影响用户体验
        });
    },
    // 显示课程详情对话框
    showCourseDetailDialog(course) {
      this.currentCourse = course;
      this.showCourseDetail = true;
    },
    getCoursesByDayAndTime(dayId, timeId) {
      // 根据dayId和timeId过滤课程
      const timeSlot = this.timeSlots.find(t => t.id === timeId);
      if (!timeSlot) return [];
      
      return this.courses.filter(course => {
        // 检查星期是否匹配
        if (parseInt(course.day_of_week) !== dayId) {
          return false;
        }
        
        // 提取课程开始时间的小时和分钟部分（忽略秒数）
        const courseStartTime = course.start_time.substring(0, 5);
        
        // 改进时间匹配逻辑：
        // 1. 检查课程开始时间是否与时间槽开始时间完全匹配
        // 2. 或者检查课程开始时间是否在时间槽的时间段内
        const isExactMatch = courseStartTime === timeSlot.start;
        
        // 将时间转换为分钟数，方便比较
        const toMinutes = (timeStr) => {
          const [hours, minutes] = timeStr.split(':').map(Number);
          return hours * 60 + minutes;
        };
        
        const courseStartMinutes = toMinutes(courseStartTime);
        const slotStartMinutes = toMinutes(timeSlot.start);
        const slotEndMinutes = toMinutes(timeSlot.end);
        
        const isInTimeSlot = courseStartMinutes >= slotStartMinutes && courseStartMinutes < slotEndMinutes;
        
        return isExactMatch || isInTimeSlot;
      });
    },
    getDayName(dayId) {
      const day = this.weekDays.find(d => d.id === dayId);
      return day ? day.name : '';
    },
    getRandomColor(id) {
      // 生成随机颜色，用于区分不同课程
      const colors = ['#FFB6C1', '#87CEFA', '#98FB98', '#F0E68C', '#DDA0DD', '#FFA07A'];
      return colors[parseInt(id) % colors.length];
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
        // 检查课程是否是模拟课程（ID在900+范围内）
        const isMockCourse = parseInt(course.id) >= 900;
        
        if (isMockCourse) {
          // 如果是模拟课程，直接从前端课程列表中删除，不需要调用API
          this.courses = this.courses.filter(c => c.id !== course.id);
          this.$message.success('课程删除成功');
        } else {
          // 如果是用户添加的课程，调用API删除
          this.$axios.delete(`/timetable/courses/${course.id}/`)
            .then(() => {
              this.courses = this.courses.filter(c => c.id !== course.id);
              this.$message.success('课程删除成功');
            })
            .catch(error => {
              console.error('删除课程失败:', error);
              this.$message.error('删除课程失败，请稍后重试');
            });
        }
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