<template>
  <div class="wrapper">
    <el-table class="inst-resource-list" :data="tableData" height="100%" empty-text="No Instrument Resource">
      <el-table-column type="expand">
        <template slot-scope="props">
          <el-form class="details" label-position="left" inline label-width="9.375vw">
            <el-form-item label="Model">
              <span>{{ props.row.model }}</span>
            </el-form-item>
            <el-form-item label="Brand">
              <span>{{ props.row.brand }}</span>
            </el-form-item>
            <el-form-item class="detail" v-for="(detail, key) in props.row.details" :key="key" :label="key" label-width="9.375vw">
              <span>{{ detail.toString() }}</span>
            </el-form-item>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column prop="label" label="Label" width="120px" :sortable="true"></el-table-column>
      <el-table-column prop="type" label="Type" width="100px" :sortable="true"></el-table-column>
      <el-table-column prop="model" label="Model" width="160px" :sortable="true"></el-table-column>
      <el-table-column prop="resource" label="Resource Name" min-width="240px"></el-table-column>
      <el-table-column prop="params" label="Params" min-width="100px" class-name="col-params"></el-table-column>
      <el-table-column label="Manage" width="100px">
        <template slot-scope="scope">
          <i class="el-icon-far fa-edit" title="Edit" @click="modInstResource(scope.row.label)"></i>
          <i class="el-icon-far fa-trash-alt" title="Remove" @click="removeInstResource(scope.row.label)"></i>
        </template>
      </el-table-column>
    </el-table>
    <div class="add-inst-wrapper">
      <el-button class="add-inst" type="success" plain @click="addInstResource"><i class="el-icon-fa-plus"></i> Add new instrument resource</el-button>
    </div>

    <el-dialog class="dlg" :title="dlg.title" :visible="dlg.visible" :before-close="dlgCancel" :close-on-click-modal="false" width="40vw">
      <el-form class="dlg-form" :inline="true" label-position="top" ref="editForm" :rules="editorRules" :model="editorData">
        <el-form-item label="Label" class="form-half" prop="label">
          <el-input v-model="editorData.label" :clearable="true" :minlength="3" :maxlength="20" placeholder="Label for resource"></el-input>
        </el-form-item>
        <el-form-item label="Type/Model" class="form-half" prop="typeModel" :disabled="dialogStatus === 'mod'">
          <el-cascader v-model="editorData.typeModel" placeholder="Choose type and model" @change="onTypeModelChange"
                       :disabled="dialogStatus==='mod'" :options="editorData.typeModelOptions"
          >
          </el-cascader>
        </el-form-item>
        <el-form-item label="Resource Name (Address)" prop="resName" class="form-whole">
          <el-input v-model="editorData.resName" :clearable="true" :maxlength="128"
                    placeholder="Instrument resource-name (address)"
          >
          </el-input>
        </el-form-item>
        <el-form-item class="form-half" v-for="(param, index) in editorData['params']" :label="param.name"
                      :key="param.name" :prop="'params.'+index+'.value'"
                      :rules="[{required: true, message:'Param \'' + param.name + '\' is required', trigger: 'change'}]"
        >
          <el-select v-if="param.type=='bool'" v-model="param.value">
            <el-option label="Enable" :value="true"></el-option>
            <el-option label="Disable" :value="false"></el-option>
          </el-select>
          <el-select v-else-if="param.options" v-model="param.value" placeholder="Select param">
            <el-option v-for="choice in param.options" :label="escapeOption(choice)" :value="choice" :key="choice"></el-option>
          </el-select>
          <el-input-number v-else-if="param.type==='int'" v-model="param.value" :min="param.min !== undefined ? param.min : -Infinity" :max="param.max !== undefined ? param.max : Infinity" label="Input param" :precision="0"></el-input-number>
          <el-input v-else v-model="param.value" placeholder="Input param"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dlg-footer">
        <el-button @click="dlgCancel">Cancel</el-button>
        <el-button type="primary" @click="dlgConfirm" :disabled="confirmStatus">Confirm</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data () {
    return {
      resources: [],
      dialogStatus: 'hidden',
      confirmStatus: false,
      editorData: {
        oldLabel: '',
        label: '',
        typeModel: [],
        resName: '',
        params: [],
        typeModelOptions: []
      },
      editorRules: {
        label: [
          { required: true, message: 'Please input a label', trigger: 'change,blur' },
          { min: 3, max: 32, message: 'Length between 3-32 characters', trigger: 'change' }
        ],
        typeModel: [
          { required: true, message: 'Please select type and model', trigger: 'change' }
        ],
        resName: [
          { required: true, message: 'Please input resource name', trigger: 'change,blur' }
        ]
      }
    }
  },
  computed: {
    dlg: function () {
      const self = this
      if (self.dialogStatus === 'mod') {
        return { title: 'Modify Instrument Resource', visible: true }
      }
      if (self.dialogStatus === 'add') {
        return { title: 'Add Instrument Resource', visible: true }
      }
      return { title: 'Instrument Resource', visible: false }
    },
    tableData () {
      const self = this
      const res = self.resources
      const tData = res.map((value) => {
        const params = value[6]
        const paramStr = Object.keys(params).reduce((prev, curr) => {
          return prev + curr + ': ' + params[curr] + '; '
        }, '')
        const tempObj = {
          label: value[0],
          type: value[1],
          model: value[2],
          brand: value[3],
          resource: value[5],
          params: paramStr,
          details: value[7]
        }
        return tempObj
      })
      return tData
    }
  },
  methods: {
    setConfirmStatus () {
      const self = this
      setTimeout(() => {
        self.confirmStatus = false
      }, 300)
    },
    removeInstResource (label) {
      const self = this
      this.$confirm('Instrument resource "' + label + '" will be removed. Continue?', 'Warning', {
        confirmButtonText: 'Remove',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }).then(() => {
        self.$rpcClient.request({
          route: ':instrument:resource:remove',
          args: [label]
        }).then(res => {
          let i
          for (i in self.resources) {
            if (self.resources[i][0] === label) {
              self.resources.splice(i, 1)
              self.$message({
                type: 'success',
                message: 'Removed Successfully'
              })
              return
            }
          }
          self.$alert('The instrument resource does not exist.', 'Error', {
            confirmButtonText: 'OK',
            type: 'error'
          })
        }).catch(err => {
          self.$alertError(err)
        })
      })
    },
    escapeOption (s) {
      let escaped = s
      if (typeof s === 'string') {
        escaped = s.replace(/\r/g, '<CR>').replace(/\n/g, '<LF>')
      }
      return escaped
    },
    addInstResource () {
      const self = this
      self.editorData = Object.assign({}, self.editorData, {
        oldLabel: '',
        label: '',
        typeModel: [],
        resName: '',
        params: []
      })
      if (self.$refs.editForm) {
        self.$refs.editForm.resetFields()
      }
      self.dialogStatus = 'add'
    },
    onTypeModelChange (value) {
      const self = this
      const model = value[1]
      self.$rpcClient.request({
        route: ':instrument:lib:get-model-info',
        args: [model]
      }).then(res => {
        const params = res[3]
        let i
        for (i in params) {
          params[i].value = ''
        }
        self.editorData.params = params
      }).catch(err => {
        self.$alertError(err)
      })
    },
    modInstResource (label) {
      const self = this
      let inst
      let i
      for (i in self.resources) {
        if (self.resources[i][0] === label) {
          inst = self.resources[i]
          break
        }
      }
      self.$rpcClient.request({
        route: ':instrument:lib:get-model-info',
        args: [inst[2]]
      }).then(res => {
        self.editorData.oldLabel = label
        self.editorData.label = label
        self.editorData.typeModel = [inst[1], inst[2]]
        self.editorData.resName = inst[5]
        const paramList = res[3]
        let i
        for (i in paramList) {
          paramList[i].value = inst[6][paramList[i].name]
        }
        self.editorData.params = paramList
      }).catch(err => {
        self.$alertError(err)
      }).finally(() => {
        self.dialogStatus = 'mod'
      })
    },
    dlgCancel () {
      const self = this
      self.dialogStatus = 'hidden'
    },
    dlgConfirm () {
      const self = this
      self.$refs.editForm.validate((valid) => {
        if (valid && (!self.confirmStatus)) {
          self.dlgSubmit()
          self.confirmStatus = true
        }
      })
    },
    dlgSubmit () {
      const self = this
      const eData = self.editorData
      if (eData.oldLabel === eData.label) {
        const config = {
          resource_name: eData.resName,
          params: {}
        }
        let i
        for (i in eData.params) {
          config.params[eData.params[i].name] = eData.params[i].value
        }
        self.$rpcClient.request({
          route: ':instrument:resource:mod',
          args: [eData.label, config]
        }).then(res => {
          self.refreshInstRes()
          self.dialogStatus = 'hidden'
        }).catch(err => {
          self.$alertError(err)
        }).finally(() => {
          self.setConfirmStatus()
        })
      } else {
        const resLabelList = self.resources.map((item) => item[0])
        if (resLabelList.indexOf(eData.label) > -1) {
          self.$alert('This label already exists for other instrument resource!\nPlease select another label.', 'Alert', {
            confirmButtonText: 'Ok',
            callback: () => {
              self.setConfirmStatus()
            }
          })
        } else {
          const params = {}
          let i
          for (i in eData.params) {
            params[eData.params[i].name] = eData.params[i].value
          }
          self.$rpcClient.request({
            route: ':instrument:resource:add',
            args: [eData.label, eData.typeModel[0], eData.typeModel[1], eData.resName, params]
          }).then(res => {
            if (self.dialogStatus === 'mod') {
              self.$rpcClient.request({
                route: ':instrument:resource:remove',
                args: [eData.oldLabel]
              }).then(res => {
                self.refreshInstRes()
                self.dialogStatus = 'hidden'
              }).catch(err => {
                self.$alertError(err)
              }).finally(() => {
                self.setConfirmStatus()
              })
            } else {
              self.refreshInstRes()
              self.dialogStatus = 'hidden'
              self.setConfirmStatus()
            }
          }).catch(err => {
            self.$alertError(err)
            self.setConfirmStatus()
          })
        }
      }
    },
    refreshInstRes () {
      const self = this
      self.$rpcClient.request({
        route: ':instrument:resource:get'
      }).then(res => {
        self.resources = res
      }).catch(err => {
        self.$alertError(err)
      })
    },
    refreshTypeModelOptions () {
      const self = this
      self.$rpcClient.request({
        route: ':instrument:lib:get-type-model-map'
      }).then(res => {
        const options = []
        let i
        for (i in res) {
          const managedModels = res[i].models.map((curr) => {
            return { label: curr, value: curr }
          })
          const managedObj = { value: res[i].type, label: res[i].type, children: managedModels }
          options.push(managedObj)
        }
        self.editorData.typeModelOptions = options
      }).catch(err => {
        this.$alertError(err)
      })
    }
  },
  created: function () {
    const self = this
    self.refreshInstRes()
    self.refreshTypeModelOptions()
  }
}
</script>

<style scoped>
  .wrapper {
    height: 100%;
    overflow: auto;
    display: flex;
    flex-direction: column;
  }

  .details.el-form {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
  }

  .details .el-form-item {
    display: flex;
    align-items: center;
    width: 50%;
    margin: 8px 0;
    flex-shrink: 0;
  }

  .details .el-form-item ::v-deep .el-form-item__label {
    color: #909399;
    padding-left: 10px;
    text-transform: capitalize;
  }

  .details .el-form-item ::v-deep .el-form-item__label, .details .el-form-item >>> .el-form-item__content {
    line-height: 20px;
  }

  .inst-resource-list ::v-deep .col-params .cell {
    word-break: normal;
  }

  .fa-edit, .fa-trash-alt {
    font-size: 16px;
    padding: 8px;
    cursor: pointer;
  }

  .fa-edit {
    color: #3a8ee6;
  }

  .fa-trash-alt {
    color: #ff4d51;
  }

  .dlg .el-dialog__body {
    padding-top: 0;
  }

  .dlg >>> .el-dialog {
    max-width: 100%;
  }

  .dlg-form {
    display: inline-flex;
    flex-wrap: wrap;
  }

  .dlg-form .form-half {
    width: 50%;
    margin-right: 0 !important;
    padding: 0 10px;
  }

  .dlg-form .form-whole {
    width: 100%;
    margin-right: 0 !important;
    padding: 0 10px;
  }

  .add-inst-wrapper {
    padding: 12px 16px;
  }

  .add-inst {
    width: 100%;
  }
</style>

<style>
</style>
