// JavaScript for handling the new goal creation flow
// look, i commented the python files, i'm get a pass here.

const stageModalTemplate = document.getElementById('stageModalTemplate').cloneNode(true);
const editStageModalTemplate = document.getElementById('editStageModalTemplate').cloneNode(true);

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
    updateStageList();
    modal.remove();
}

function updateStage(index) {
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
    stages[index]={title: title, description: description, tasks: tasks, milestone: milestone, duration: duration};
    console.log("[new_goal.js] Stage updated at index: " + index);
    closeModal('stageModal');
    updateStageList();
    modal.remove();
}

function deleteStage(index) {
    if (index < 0 || index >= stages.length) {
        console.error("[new_goal.js] Invalid stage index: " + index);
        return;
    }
    stages.splice(index, 1);
    console.log("[new_goal.js] Stage deleted at index: " + index);
    updateStageList();
}

function editStage(index) {
    console.log("[new_goal.js] Edit stage at index: " + index);
    var stage = stages[index];
    var modal = editStageModalTemplate.cloneNode(true);
    modal.id = 'stageModal'
    modal.hidden = false;
    document.getElementById('stageModalContainer').appendChild(modal);
    modal.querySelector('input[name="stageTitle"]').value = stage.title;
    modal.querySelector('textarea[name="stageDescription"]').value = stage.description;
    modal.querySelector('input[name="stageDuration"]').value = stage.duration;
    stage.tasks.forEach(taskdata => {
        console.log('[new_goal.js] Adding task to edit modal: ', task);
        var taskList = document.getElementById('tasksList');
        var task = htmlToNodes('<li><input name="title" placeholder="Task Title"><input type="text" name="description" placeholder="Task Description"><select name="timeperiod"><option selected value="daily">Daily</option><option value="weekly">Weekly</option></select><select name="optional"><option selected value="required">Required</option><option value="optional">Optional</option></select></li>');
        task.querySelector('input[name="title"]').value = taskdata.title;
        task.querySelector('input[name="description"]').value = taskdata.description;
        task.querySelector('select[name="timeperiod"]').value = taskdata.type;
        if (taskdata.optional) {
            task.querySelector('select[name="optional"]').value = "optional";
        } else {
            task.querySelector('select[name="optional"]').value = "required";
        }
        taskList.appendChild(task);
    });
    modal.querySelector('input[name="milestoneTitle"]').value = stage.milestone[0];
    modal.querySelector('input[name="milestoneDescription"]').value = stage.milestone[1];
    modal.querySelector('button[name="update"]').setAttribute('onclick', 'updateStage(' + index + ')');
    openModal('stageModal');
}

function updateStageList() {
    const stageList = document.getElementById("stages");
    stageList.innerHTML = "";
    stages.forEach((stage, index) => {
        var stageContainer = htmlToNodes("<div class=\"card\"><b><p name=\"title\">" + stage.title + "</p></b><p name=\"description\">" + stage.description + "</p><p name=\"duration\">" + stage.duration + " week/s</p><span><button onclick='editStage(" + index + ")'>Edit</button><button onclick='deleteStage(" + index + ")'>Delete</button></span><br><br></div>");
        stageList.appendChild(stageContainer);
    })
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

function addExample() {
    stages.push({"title":"title","description":"desc","tasks":[{"title":"asdfasd","description":"asdas","type":"daily","optional":false},{"title":"asdf","description":"fdssgh","type":"weekly","optional":true}],"milestone":["asdgfd","ghhfgj"],"duration":"1"});
    updateStageList();
    console.log("[new_goal.js] Example data added");
}

function sendit() {
    console.log("[new_goal.js] Send it!");
    console.log("[new_goal.js] Stages: ", stages);
    try {
        if (stages.length == 0) {
            throw "No stages added";
        }
        var title = document.querySelector('input[name="title"]').value;
        var description = document.querySelector('textarea[name="description"]').value;
    } catch (error) {
        console.error("[new_goal.js] Error getting goal data: " + error);
        document.getElementById('formError').removeAttribute('hidden');
        return;
    }
    // put into the form
    var form = document.getElementById('theForm');
    form.querySelector('input[name="title"]').value = title;
    form.querySelector('input[name="description"]').value = description;
    form.querySelector('input[name="stages"]').value = JSON.stringify(stages);
    form.submit();
}