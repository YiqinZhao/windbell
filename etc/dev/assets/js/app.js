function EnviromentsPool (data) {
  this.pool = JSON.parse(JSON.stringify(data))
}

EnviromentsPool.prototype.render = function () {
  function envFactory (env, idx) {
    return `<tr class="env-item" data-idx="${idx}">
        <td class="collapsing" onclick="onEnvDeleteClick(${idx})">
            <i class="trash icon red env-remove"></i>
        </td>
        <td class="collapsing env-key"
            data-idx="${idx}"
            onclick="onEnvItemClick('key', ${idx})">
          <p class="key-content">${env.key}</p>
          <div class="ui input hide env-input">
              <input type="text" onblur="onEnvItemBlur('key', ${idx})">
          </div>
        </td>
        <td class="env-value"
            data-idx="${idx}"
            onclick="onEnvItemClick('value', ${idx})">
            <p class="value-content">${env.value}</p>
            <div class="ui input hide env-input">
                <input type="text" onblur="onEnvItemBlur('value', ${idx})">
            </div>
        </td>
    </tr>`
  }

  return this.pool
    .map((v, i) => envFactory(v, i))
    .join('')
}

EnviromentsPool.prototype.push = function (key, value) {
  this.pool.push({ key, value })
}

EnviromentsPool.prototype.set = function (key, idx, value) {
  this.pool[idx][key] = value
}

EnviromentsPool.prototype.deleteAtIndex = function (index) {
  this.pool.splice(index, 1)
}

EnviromentsPool.prototype.export = function (index) {
  return JSON.stringify(this.pool)
}

var editor = ace.edit('editor')
var envPool, windfileStorage, activeContent

window.onload = function () {
  Split(['#left', '#right'], {
    gutterStyle: (dimension, gutterSize) => ({
      'width': '2px'
    })
  })
  $('.menu .item').tab()
  $('.ui.dropdown').dropdown()

  $('#test-modal').modal({
    onApprove: function (data) {
      showFloatMessage(
        'Just one second',
        'We\'re sending test email for you.',
        'notched loading circle',
        autoDismiss = false
      )

      var to = $('#receiver-dropdown').dropdown('get value')
      $.ajax({
        url: '/send',
        method: 'POST',
        data: {
          to,
          envs: envPool.export(),
          config: windfileStorage.config,
          template: windfileStorage.template
        },
        success: function (data) {
          if (data.ok) {
            showFloatMessage(
              'Finished!',
              'We\'re have sent a testing email for you.',
              'check',
              autoDismiss = true,
              startAnimation = false
            )
          } else {
            showFloatMessage(
              'Error!',
              data.msg,
              'close',
              autoDismiss = false,
              startAnimation = false
            )
          }
        }
      })
    }
  })

  editor.setTheme('ace/theme/chrome')
  editor.session.setMode('ace/mode/yaml')

  fetchWindfile()
}

$(document).keydown(function (event) {
  if ((event.ctrlKey || event.metaKey) && event.which == 83) {
    event.preventDefault()
    onSaveButtonClick()
    return false
  } else if ((event.ctrlKey || event.metaKey) && event.which == 69) {
    console.log(12)
    event.preventDefault()
    onTestButtonClick()
    return false
  }
})

function fetchWindfile () {
  $.ajax({
    url: '/windfile?timestamp=' + (new Date()).getTime(),
    success: function (data) {
      windfileStorage = JSON.parse(JSON.stringify(data))
      windfileStorage.envs = windfileStorage.envs
        .map(v => ({ key: v, value: `VALUE_${v}` }))

      activeContent = 'config'

      editor.setValue(data.config)
      editor.on('change', onWindfileChange)

      envPool = new EnviromentsPool(windfileStorage.envs)
      $('#env-table-body').html(envPool.render())

      onWindfileChange()
    }
  })
}

function onWindfileChange () {
  var v = editor.getValue()
  if (v.length === 0) return

  windfileStorage[activeContent] = editor.getValue()
  $.ajax({
    url: '/windfile',
    method: 'POST',
    data: {
      config: windfileStorage.config,
      template: windfileStorage.template,
      envs: envPool.export()
    },
    success: function (data) {
      $('#preview-frame').attr('srcdoc', data.rendered)
    }
  })
}

function onMenuClick (idx) {
  $('.menu > .item').removeClass('active')
  $('.menu > .item[data-idx=' + idx + ']').addClass('active')

  if (idx === 0) {
    $('#env-table').removeClass('hide')
    $('#editor').addClass('hide')
  } else {
    $('#env-table').addClass('hide')
    $('#editor').removeClass('hide')
  }

  if (idx === 1) {
    activeContent = 'config'
    editor.session.setMode('ace/mode/yaml')
    editor.setValue(windfileStorage.config)
  } else if (idx == 2) {
    activeContent = 'template'
    editor.session.setMode('ace/mode/html')
    editor.setValue(windfileStorage.template)
    editor.setValue(windfileStorage.template)
  }
}

function onEnvItemClick (type, idx) {
  let target = $('.env-' + type + '[data-idx=' + idx + ']')
  let childrens = target.children()

  let content = childrens[0]
  let input = childrens[1]

  let v = $(content).text().trim()

  if ($(content).hasClass('hide')) return

  $(content).text('')
  $(content).addClass('hide')
  $(input).removeClass('hide')
  $($(input).children()[0]).focus()
  $($(input).children()[0]).attr('value', v)
}

function onEnvItemBlur (type, idx) {
  let target = $('.env-' + type + '[data-idx=' + idx + ']')
  let childrens = target.children()

  let content = childrens[0]
  let input = childrens[1]

  let v = $($(input).children()[0]).val().trim()
  envPool.set(type, idx, v)
  $('#env-table-body').html(envPool.render())
  onWindfileChange()

  $(content).text(v)
  $(content).removeClass('hide')
  $(input).addClass('hide')
}

function onEnvAddClick () {
  envPool.push('ENV_NAME', 'ENV_VALUE')
  $('#env-table-body').html(envPool.render())
}

function onEnvDeleteClick (idx) {
  envPool.deleteAtIndex(idx)
  $('#env-table-body').html(envPool.render())
}

function showFloatMessage (title, content, icon,
  autoDismiss = true, startAnimation = true) {
  $('.float-message-icon')
    .removeClass()
    .addClass('float-message-icon')
    .addClass('icon ' + icon)
  if (startAnimation) $('.float-message').transition('scale')
  $('.float-message-title').text(title)
  $('.float-message-content').text(content)
  if (autoDismiss) {
    setTimeout(() => {
      $('.float-message').transition('scale')
    }, 750)
  } else {
    $('.float-message .close').on('click', function () {
      $(this)
        .closest('.message')
        .transition('scale')
    })
  }
}

function onSaveButtonClick () {
  showFloatMessage(
    'Just one second',
    'We\'re saving content for you.',
    'notched loading circle',
    autoDismiss = false
  )

  $.ajax({
    url: '/windfile',
    method: 'PUT',
    data: {
      config: windfileStorage.config,
      template: windfileStorage.template
    },
    success: function (data) {
      showFloatMessage(
        'Finished!',
        'Your windfile has been saved!',
        'check',
        autoDismiss = true,
        startAnimation = false
      )
    }
  })
}

function onTestButtonClick () {
  $.ajax({
    url: '/receiver',
    method: 'POST',
    data: {
      config: windfileStorage.config
    },
    success: function (data) {
      var receivers = data.receivers
      var receiverList = '<option value="">Receiver</option>' +
                    receivers
                      .map(v => `<option value="${v}">${v}</option>`)
      $('#receiver-dropdown').html(receiverList)
      $('#receiver-dropdown').dropdown()
      $('.ui.modal').modal('show')
    }
  })
}
