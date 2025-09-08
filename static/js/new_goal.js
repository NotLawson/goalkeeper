// JavaScript for handling the new goal creation flow
const stageModalTemplate = document.getElementById('stageModalTemplate').cloneNode(true);
var stages = [];

function newStage() {
    console.log("[new_goal.js] Adding new stage");
    var modal = stageModalTemplate.cloneNode(true);
    modal.id = 'stageModal'
    modal.hidden = false;
    document.getElementById('stageModalContainer').appendChild(modal);
    openModal('stageModal');
}

function saveStage() {
    var modal = document.getElementById('stageModal');
    //try {
        var title = modal.querySelector('input[name="stageTitle"]').value;
        var description = modal.querySelector('textarea[name="stageDescription"]').value;
        var duration = modal.querySelector('input[name="stageDuration"]').value;
        var taskElements = []; document.getElementById('tasksList').childNodes.forEach(x => {if (x.tagName === "LI"){taskElements.push(x)}});
        var tasks = [];
        taskElements.forEach(x => {
            var title = x.querySelector('input[name="title"]').value;
            var description = x.querySelector('input[name="description"]').value;
            var timeperiod = x.querySelector('select[name="timeperiod"]').value;
            if (x.querySelector('select[name="optional"]').value == "optional") {var optional = true} else {var optional = false};
            tasks.push({title: title, description: description, type: timeperiod, optional: optional});
        });
        var milestone = [modal.querySelector('input[name="milestoneTitle"]').value, modal.querySelector('input[name="milestoneDescription"]').value];
    ///} catch (error) {
    //    modal.querySelector('p[name="error"]').removeAttribute('hidden');
    //    console.error("[new_goal.js] Error saving stage: " + error);
    //    return;
    //}
    stages.push({title: title, description: description, tasks: tasks, milestone: milestone, duration: duration});
    console.log("[new_goal.js] New stage added");
    closeModal('stageModal');
    modal.remove();
}

// adapted from from https://stackoverflow.com/questions/494143/creating-a-new-dom-element-from-an-html-string-using-built-in-dom-methods-or-pro
function htmlToNodes(html) {
    const template = document.createElement('template');
    template.innerHTML = html;
    return template.content.childNodes[0];
}

function newTask() {
    console.log("[new_goal.js] Adding new task");
    var taskList = document.getElementById('tasksList');
    var task = htmlToNodes('<li><input name="title" placeholder="Task Title"><input type="text" name="description" placeholder="Task Description"><select name="timeperiod"><option selected value="daily">Daily</option><option value="weekly">Weekly</option></select><select name="optional"><option selected value="required">Required</option><option value="optional">Optional</option></select></li>');
    taskList.appendChild(task);
}