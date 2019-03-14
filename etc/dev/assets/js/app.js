function EnviromentsPool (data) {
  this.pool = JSON.parse(JSON.stringify(data))
}

EnviromentsPool.prototype.render = function () {
  function envFactory (env, idx) {
    return `<tr class="env-item" data-idx="${idx}">
        <td class="collapsing" onclick="onEnvDeleteClick(${idx})">
            <i class="trash icon red env-remove"></i>
        </td>
        <td class="collapsing">${env.key}</td>
        <td class="env-value" data-idx="${idx}" onclick="onEnvValueClick(${idx})">
            <p class="value-content">${env.value}</p>
            <div class="ui input hide">
                <input type="text" onblur="onEnvInputBlur(${idx})">
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

EnviromentsPool.prototype.setValue = function (idx, value) {
  this.pool[idx].value = value
}

EnviromentsPool.prototype.deleteAtIndex = function (index) {
  this.pool.splice(index, 1)
}

EnviromentsPool.prototype.export = function (index) {
  return JSON.stringify(this.pool)
}
