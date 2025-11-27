<template>
  <div class="timetable-import-container">
    <h2>导入课程</h2>
    <div class="import-content">
      <el-card class="import-card">
        <div slot="header" class="clearfix">
          <span>导入说明</span>
        </div>
        <div class="import-instructions">
          <ol>
            <li>请下载课程表模板文件</li>
            <li>按照模板格式填写课程信息</li>
            <li>上传填写好的Excel文件</li>
            <li>系统将自动导入课程数据</li>
          </ol>
          <el-button type="primary" @click="downloadTemplate" style="margin-top: 20px;">
            <i class="el-icon-download"></i> 下载模板
          </el-button>
        </div>
      </el-card>

      <el-card class="import-card">
        <div slot="header" class="clearfix">
          <span>上传文件</span>
        </div>
        <div class="upload-section">
          <el-upload
            class="upload-demo"
            drag
            action="#"
            :auto-upload="false"
            :on-change="handleFileChange"
            :before-upload="beforeUpload"
            accept=".xlsx,.xls"
            :file-list="fileList"
          >
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
            <div class="el-upload__tip" slot="tip">仅支持 .xlsx 和 .xls 格式的Excel文件</div>
          </el-upload>
          
          <div class="upload-actions" v-if="fileList.length > 0">
            <el-button type="primary" @click="handleUpload">开始导入</el-button>
            <el-button @click="clearFiles">清空</el-button>
          </div>
        </div>
      </el-card>

      <!-- 导入结果 -->
      <el-card v-if="showResult" class="import-card result-card">
        <div slot="header" class="clearfix">
          <span>导入结果</span>
        </div>
        <div class="result-content">
          <el-alert
            :title="result.success ? '导入成功' : '导入失败'"
            :type="result.success ? 'success' : 'error'"
            show-icon
          ></el-alert>
          <div v-if="result.message" class="result-message">
            {{ result.message }}
          </div>
          <div v-if="result.details" class="result-details">
            <h4>详细信息：</h4>
            <ul>
              <li v-for="(detail, index) in result.details" :key="index">
                {{ detail }}
              </li>
            </ul>
          </div>
          <div class="result-actions">
            <el-button type="primary" @click="$router.push('/timetable')">查看课程表</el-button>
            <el-button @click="resetImport">重新导入</el-button>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TimetableImport',
  data() {
    return {
      fileList: [],
      showResult: false,
      result: {
        success: false,
        message: '',
        details: []
      }
    }
  },
  methods: {
    downloadTemplate() {
      // 这里应该实现模板下载逻辑
      this.$message.info('模板下载功能开发中')
    },
    handleFileChange(file, fileList) {
      this.fileList = fileList
    },
    beforeUpload(file) {
      const isExcel = file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' || file.type === 'application/vnd.ms-excel'
      const isLt2M = file.size / 1024 / 1024 < 2

      if (!isExcel) {
        this.$message.error('上传文件只能是 Excel 格式!')
      }
      if (!isLt2M) {
        this.$message.error('上传文件大小不能超过 2MB!')
      }
      return isExcel && isLt2M
    },
    handleUpload() {
      if (this.fileList.length === 0) {
        this.$message.warning('请先选择要上传的文件')
        return
      }

      // 模拟导入过程
      this.$message.info('开始导入课程数据...')
      
      // 模拟异步导入
      setTimeout(() => {
        // 模拟导入结果
        this.result = {
          success: true,
          message: '课程导入成功',
          details: [
            '成功导入 5 门课程',
            '高等数学 - 导入成功',
            '大学英语 - 导入成功',
            '计算机导论 - 导入成功',
            '大学物理 - 导入成功',
            '线性代数 - 导入成功'
          ]
        }
        this.showResult = true
      }, 2000)
    },
    clearFiles() {
      this.fileList = []
    },
    resetImport() {
      this.fileList = []
      this.showResult = false
      this.result = {
        success: false,
        message: '',
        details: []
      }
    }
  }
}
</script>

<style scoped>
.timetable-import-container {
  padding: 20px;
}

.import-content {
  max-width: 800px;
}

.import-card {
  margin-bottom: 20px;
}

.import-instructions {
  line-height: 1.8;
  color: #606266;
}

.import-instructions ol {
  padding-left: 20px;
}

.upload-section {
  text-align: center;
  padding: 30px 0;
}

.upload-actions {
  margin-top: 20px;
}

.result-content {
  padding: 20px 0;
}

.result-message {
  margin: 20px 0;
  padding: 10px;
  background: #f0f9eb;
  border: 1px solid #e1f3d8;
  border-radius: 4px;
  color: #67c23a;
}

.result-details {
  margin: 20px 0;
  padding: 10px;
  background: #ecf5ff;
  border: 1px solid #d9ecff;
  border-radius: 4px;
}

.result-details h4 {
  margin-top: 0;
  color: #409eff;
}

.result-details ul {
  padding-left: 20px;
  color: #606266;
}

.result-actions {
  margin-top: 20px;
  text-align: center;
}
</style>