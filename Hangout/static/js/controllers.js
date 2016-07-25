(function () {
  'use strict';

  var CONST = {
        WEEK: ['SUN','MON','TUE','WED','THU','FRI','SAT'],
        TIME_SEG: ['0:00-7:00', '7:00-12:00', '12:00-18:00', '18:00-24:00']
    };

  angular.module('hangout.controllers', [])
    .controller('homepageCtrl', ['$scope', '$location', function($scope, $location){
      console.log('homepage');
      $scope.login = function(){
        $location.url('/login');
      }
    }])
    .controller('loginCtrl', ['$scope', '$location', 'Authentication', function($scope, $location, Authentication){
      console.log('login');
      var vm = this;
      vm.login = login;
      activate();
      function activate() {
        if (Authentication.isAuthenticated()) {
          $location.url('/');
        }
      }
      function login() {
        Authentication.login(vm.email, vm.password);
      }
    }])
    .controller('registerCtrl', ['$scope', '$location', 'Authentication', function($scope, $location, Authentication){
      console.log('register');
      var vm = this;
      vm.tags = "student";
      vm.register = register;
      function register() {
        Authentication.register(vm.email, vm.password, vm.username, encodeFixedTime(), $('#register__tags').val(), vm.cellphone, vm.intro);
      }
      activate();
      function activate() {
        if (Authentication.isAuthenticated()) {
          $location.url('/');
        }
      }
      //FixedTimeTable
      vm.week = CONST.WEEK;
      vm.times = CONST.TIME_SEG;
      $scope.$on('ngRepeatFinished', function (ngRepeatFinishedEvent) {
          var tds = $('#register__fixed').find('td');
          tds.click(function () {
              onSelectTime(tds.index($(this)), "register");
          });
      });
      //js-lib: tagsinput
      $.getScript('/static/lib/bootstrap-tagsinput/bootstrap-tagsinput.js');
    }])
    .controller('profileCtrl', ['$scope', '$location', 'Authentication', '$http', function($scope, $location, Authentication, $http){
      console.log('profile');
      if (Authentication.isAuthenticated()) {
        var vm = this;
        vm.update_profile = function() {
          Authentication.update_profile(vm.email, vm.password, vm.username, encodeFixedTime(), $('#profile__tags').val(), vm.cellphone, vm.intro);
        };
        vm.email = Authentication.getAuthenticatedAccount().user_info.email;
        vm.password = Authentication.getAuthenticatedAccount().user_info.password;
        vm.username = Authentication.getAuthenticatedAccount().user_info.name;
        vm.fix_times = Authentication.getAuthenticatedAccount().user_info.fix_times;
        vm.tags = Authentication.getAuthenticatedAccount().user_info.tags;
        vm.cellphone = Authentication.getAuthenticatedAccount().user_info.cellphone;
        vm.intro = Authentication.getAuthenticatedAccount().user_info.intro;        
        //js-lib: tagsinput
        $.getScript('/static/lib/bootstrap-tagsinput/bootstrap-tagsinput.js');
      }
      else {
        $location.url('/login');
      }
      //FixedTimeTable
      vm.week = CONST.WEEK;
      vm.times = CONST.TIME_SEG;
      $scope.$on('ngRepeatFinished', function (ngRepeatFinishedEvent) {
          var tds = $('#profile__fixed').find('td');
          tds.click(function () {
              onSelectTime(tds.index($(this)), "profile");
          });
          decodeFixedTime(vm.fix_times, "profile");
      });
    }])
    .controller('activityCtrl', ['$http', '$location', '$scope', 'Authentication', function($http, $location, $scope, Authentication){
      $(".act-nav").click(function(){
        $(".act-nav").not(this).removeClass("active");
        $(this).addClass("active");
      })
      $scope.myActs = function() {
        $scope.page_title = "组织的活动";
        $scope.act_type = "my_act";
        $('.act-nav').not('#myActs').removeClass("active");
        $('#myActs').addClass('active');
        $scope.acts = Authentication.get_profile().admin_acts;
        $scope.B = function(state) {
          return {
            0: "停止报名",
            1: "开放报名",
            2: "",
          }[state];
        }
        $scope.L2 = function(state) {
          return {
            0: "danger",
            1: "success",
            2: "",
          }[state];
        }
        $scope.U = function(state) {
          return {
            0: "danger",
            1: "success",
            2: "",
          }[state];
        }
        $scope.T = function(state) {
          return {
            0: "接受报名",
            1: "结束报名",
            2: "活动结束",
          }[state];
        }
        $scope.L1 = function(state) {
          return {
            0: "success",
            1: "danger",
            2: "default",
          }[state];
        }
      }
      $scope.joinActs = function() {
        $scope.page_title = "参与的活动";
        $scope.act_type = "part_act";
        $('.act-nav').not('#joinActs').removeClass("active");
        $('#joinActs').addClass('active');
        $scope.acts = Authentication.get_profile().coll_acts;
        $scope.acts.walk_around = $scope.otherActs;
        $scope.B = function() {
          return {
            0: "停止报名",
            1: "开放报名",
            2: "",
          }[state];
        }
        $scope.T = function(state) {
          return {
            0: "接受报名",
            1: "结束报名",
            2: "活动结束",
          }[state];
        }
        $scope.L = function(state) {
          return {
            0: "success",
            1: "danger",
            2: "default",
          }[state];
        }
      }
      $scope.orgActs = function() {
        $scope.page_title = "组织活动";
        $scope.act_type = "apply_act";
        $.getScript('/static/lib/bootstrap-tagsinput/bootstrap-tagsinput.js');
        $scope.act = {
          name: "",
          intro: "",
          location: "",
          cost: "",
        }
        $scope.apply = function() { 
          console.log($scope.act);        
          $http.post('/api/activity/create', $.param({
            'name': $scope.act.name,
            'intro': $scope.act.intro,
            'location': $scope.act.location,
            'tags': $('#apply_tags').val(),
            'cost': $scope.act.cost,
          })).then(function(){
            $scope.myActs();
          });
        }
      }
      $scope.otherActs = function() {
        $scope.page_title = "随便逛逛";
        $scope.act_type = "recommend_act";
        $('.act-nav').not('#otherActs').removeClass("active");
        $('#otherActs').addClass('active');
      }
      $scope.myActs();
    }])
    .controller('navbarCtrl', ['$location', '$scope', '$rootScope', 'Authentication', function($location, $scope, $rootScope, Authentication){
      function login() {
        $location.url('/login');
      }
      function logout() {
        Authentication.logout();
      }
      function register() {
        $location.url('/register');
      }
      $scope.activity = function() {
        $location.url('/activity');
      }
      $scope.friends = function() {
        $location.url('/friends');
      }
      $scope.register = register;
      if (Authentication.isAuthenticated()) {
        $scope.displayName = Authentication.getAuthenticatedAccount().user_info.name;
        $('#nav_user').css({'display': 'block'});
        $('#nav_register').css({'display': 'none'});
        $('#nav_activity').css({'display': 'block'});
        $('#nav_friends').css({'display': 'block'});
        $scope.logger = '登出';
        $scope.login_logout = logout;
      }
      else {
        $scope.displayName = '注册';
        $('#nav_user').css({'display': 'none'});
        $('#nav_activity').css({'display': 'none'});
        $('#nav_friends').css({'display': 'none'});
        $('#nav_register').css({'display': 'block'});
        $scope.logger = '登录';
        $scope.login_logout = login;
      }
      $rootScope.$on('login_done', function(){
        $scope.displayName = Authentication.getAuthenticatedAccount().user_info.name;
        $('#nav_user').css({'display': 'block'});
        $('#nav_register').css({'display': 'none'});
        $('#nav_activity').css({'display': 'block'});
        $('#nav_friends').css({'display': 'block'});
        $scope.logger = '登出';
        $scope.login_logout = logout;
      })
      $rootScope.$on('logout_done', function(){
        $scope.displayName = '注册';
        $('#nav_user').css({'display': 'none'});
        $('#nav_activity').css({'display': 'none'});
        $('#nav_friends').css({'display': 'none'});
        $('#nav_register').css({'display': 'block'});
        $scope.logger = '登录';
        $scope.login_logout = login;
      })
    }]);

    //FixedTimeTable
    var len = 28;
    var fixedTimeArray = [];//global
    for (var i = 0; i < len; i++) {
        fixedTimeArray.push(0);
    }

    function onSelectTime(value, type) {
        var tds = $('#' + type + '__fixed').find('td');

        if (value >= 0 && value < len) {
            fixedTimeArray[value] = 1 - fixedTimeArray[value];
        }

        if (fixedTimeArray[value] === 1) {
            tds[value].style.backgroundColor = '#FFF';
        } else {
            tds[value].style.backgroundColor = '#EBEBEB';
        }
    }

    function encodeFixedTime() {
        var binStr = '';
        for (var i = 0; i < len; i++) {
            binStr += fixedTimeArray[i];
        }
        return parseInt(binStr, 2);
    }

    function decodeFixedTime(fixedTime, type) {
        var timeStr = fixedTime.toString(2);
        var s = '';
        for (var k = 0; k < len-timeStr.length; k++) {
            s += '0';
        }
        timeStr = s + timeStr;
        var strTimeArray = timeStr.split("");
        for (var i = 0; i < len; i++) {
            fixedTimeArray[i] = parseInt(strTimeArray[i]);
        }
        
        //update view
        var tds = $('#' + type + '__fixed').find('td');
        for (var j = 0; j < len; j++) {
            if (fixedTimeArray[j] === 1) {
                tds[j].style.backgroundColor = '#FFF';
            } else {
                tds[j].style.backgroundColor = '#EBEBEB';
            }
        }
    }
})();
