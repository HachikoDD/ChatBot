var winWidth = 0,winHeight = 0; var tableheight = 0;
function changebleWidthHeight() {
    if (window.innerWidth)
        winWidth = window.innerWidth;
    else if ((document.body) && (document.body.clientWidth))
        winWidth = document.body.clientWidth;
//获取窗口高度
    if (window.innerHeight)
        winHeight = window.innerHeight;
    else if ((document.body) && (document.body.clientHeight))
        winHeight = document.body.clientHeight;
//通过深入Document内部对body进行检测，获取窗口大小
    if (document.documentElement && document.documentElement.clientHeight && document.documentElement.clientWidth)
    {
        winHeight = document.documentElement.clientHeight;
        winWidth = document.documentElement.clientWidth;
    }
    tableheight = winHeight- 55;
}
window.onresize = changebleWidthHeight();

setInterval('changebleWidthHeight()',50);

$(function () {
	$('#reportTable').bootstrapTable({
    // url: '../static/management/test.json',
    url: '/show/questions',
		method: 'get',
    dataType: "json",
    uniqueId: "id",
		cache: false,
    contentType: 'application/json,charset=utf-8',
		height: $(window).height()-55,
    classes: "table table-bordered table-striped  table-hover",
		pagination: true,
		pageSize: 15,
		pageNumber:1,
		pageList: [15, 30],  sidePagination:'client',
		search: true,
		showColumns: false,
		showRefresh: true,
		showExport: false,
		clickToSelect: true,
    paginationPreText: "Previous",
    paginationNextText: "Next",
    paginationFirstText: "First",
    paginationLastText: "Last",
		columns:
		[
			{field:"Question",title:"Question",align:"left",valign:"middle",sortable:"false"}
		],
    onClickCell: function (field, value, row, $element) {
      // alert(row.Question);
      layer.open({
      type: 2,
      title: 'Anwser Question',
      maxmin: true,
      shadeClose: true, //点击遮罩关闭层
      area : ['760px' , '630px'],
      content: 'answer_window',
      // content: 'answer.html',
      id: 'answer_window',
      success : function(layero, index){
        var body = layer.getChildFrame('body', index);
        body.find('#question_content').text(row.Question);
        body.find('#question_id').text(row.id);
      },
      end: function () {
        location.reload();
      },
    });
    }
	});
});
