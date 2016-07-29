(function () {
  'use strict';

  var CONST = {
        WEEK: ['SUN','MON','TUE','WED','THU','FRI','SAT'],
        TIME_SEG: ['08:00-12:00', '12:00-15:00', '15:00-19:00', '19:00-22:00']
    };

  angular.module('hangout.controllers', [])
    .controller('homepageCtrl', ['$rootScope', '$scope', '$location', '$http', 'Authentication', function($rootScope, $scope, $location, $http, Authentication){
      console.log('homepage');
      $('#search_content').css({
        'width': '500px',
      })
      $('#result').css({
        'display': 'none',
      })
      if (Authentication.isAuthenticated()) {
        $scope.login_user = Authentication.getAuthenticatedAccount().user_info;
      }
      $scope.join_act = function(act) {
        $http.post('/api/user/apply', $.param({
          'act_id': act.id,
          'type': 1,
        }))
      }
      $scope.search = function() {
        $http.get('/api/search/' + $scope.search_content).success(function(data) {
          console.log(data);
          $('#search_content').css({
            'width': '200px',
          })
          $('#search_form').css({
            'top': '10%',
            'left': '10%',
          })
          $('#result').css({
            'display': 'block',
          })
          $scope.acts = data.act;
          $scope.tags = data.tag;
          $scope.users = data.user;
          $http.get('/api/user/following').success(function(data) {
            console.log(data);
            $scope.follow_list = data.following;
            $scope.F = function(user_id) {
              for (var i = 0; i < $scope.follow_list.length; i++) {
                if (user_id == $scope.follow_list[i].id) {
                  return "取关";
                }
              }
              return "关注";
            }
            $scope.sendMsgTo = function(user) {
              $rootScope.getSendUser(user);
            }
            $scope.change_follow = function(user_id) {
              if ($scope.F(user_id) == "关注") {
                $http.post('/api/user/follow', $.param({'id': user_id})).success(function(data) {
                  $scope.follow_list.push(user_id);
                })
              }
              else {
                $http.post('/api/user/unfollow', $.param({'id': user_id})).success(function(data) {
                  $scope.follow_list.push(user_id);
                })
              }
            }
            $('.follow-btn').click(function(){
              if ($(this).html() == "取关") {
                $(this).html("关注");
              }
              else {
                $(this).html("取关");
              }
            })
          })
        });
      }
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
      $scope.U = function(act) {
        if (act.state == 0) {
          $http.post('/api/activity/change_state', $.param({
            'id': act.id,
            'state': 1,
          })).success(function(){
            act.state = 1;
          });
        }
        else {
          $http.post('/api/activity/change_state', $.param({
            'id': act.id,
            'state': 0,
          })).success(function(){
            act.state = 0;
          });
        }
      }
      $scope.D = function(act) {
        $http.post('/api/activity/change_state', $.param({
          'id': act.id,
          'state': 2,
        })).success(function(){
          act.state = 2;
        });
      }
      $scope.T = function(state) {
        return {
          0: "接受报名",
          1: "结束报名",
          2: "已结束",
        }[state];
      }
      $scope.L1 = function(state) {
        return {
          0: "success",
          1: "danger",
          2: "default",
        }[state];
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

      //validator
      $('#login_form').bootstrapValidator({
        fields: {
          email: {
            validators: {
              notEmpty: {
                message: '邮箱不能为空'
              },
              emailAddress: {
                message: '输入不是有效的电子邮件地址'
              }
            }
          },
          password: {
            validators: {
              notEmpty: {
                message: '密码不能为空'
              },
              stringLength: {
                min: 6,
                max: 15,
                message: '密码必须大于6，小于15个字'
              },
              regexp: {
                regexp: /^[a-zA-Z0-9_\.]+$/,
                message: '密码中含有特殊字符'
              }
            }
          }
        }
      })
      .on('success.form.bv', function(e) {
        e.preventDefault();
        if ($('#login_form').data('bootstrapValidator').isValid()) {
          vm.login();
        }
      });
    }])
    .controller('registerCtrl', ['$scope', '$location', 'Authentication', function($scope, $location, Authentication){
      console.log('register');
      var vm = this;
      vm.tags = "student";
      vm.register = register;
      function register() {
        Authentication.register(vm.email, vm.password, vm.username);
      }
      activate();
      function activate() {
        if (Authentication.isAuthenticated()) {
          $location.url('/');
        }
      }
      //validator
      $('#register_form').bootstrapValidator({
        feedbackIcons: {
          valid: 'fa fa-check',
          invalid: 'fa fa-times',
          validating: 'fa fa-refresh'
        },
        fields: {
          email: {
            validators: {
              notEmpty: {
                message: '邮箱不能为空'
              },
              emailAddress: {
                message: '输入不是有效的电子邮件地址'
              }
            }
          },
          username: {
            validators: {
              notEmpty: {
                message: '用户名不能为空'
              },
              stringLength: {
                min: 3,
                max: 10,
                message: '用户名必须大于3，小于10个字'
              }
            }
          },
          password: {
            validators: {
              notEmpty: {
                message: '密码不能为空'
              },
              stringLength: {
                min: 6,
                max: 15,
                message: '密码必须大于6，小于15个字'
              },
              regexp: {
                regexp: /^[a-zA-Z0-9_\.]+$/,
                message: '密码中含有特殊字符'
              }
            }
          },
          cfmpassword: {
            validators: {
              notEmpty: {
                message: '确认密码不能为空'
              },
              identical: {
                field: 'password',
                message: '两次密码输入不一致'
              }
            }
          },
        }
      })
      .on('success.form.bv', function(e) {
        e.preventDefault();
        if ($('#register_form').data('bootstrapValidator').isValid()) {
          vm.register();
        }
      });

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
    .controller('profileCtrl', ['$scope', '$location', 'Authentication', '$http', 'FileUploader', function($scope, $location, Authentication, $http, FileUploader){
      console.log('profile');

      //uploader
      var uploader = $scope.uploader = new FileUploader({
        url: '/api/user/update_portrait'
      });

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

      //validator
      $('#profile_form').bootstrapValidator({
        feedbackIcons: {
          valid: 'fa fa-check',
          invalid: 'fa fa-times',
          validating: 'fa fa-refresh',
        },
        fields: {
          email: {
            validators: {
              notEmpty: {
                message: '邮箱不能为空',
              },
              emailAddress: {
                message: '输入不是有效的电子邮件地址',
              }
            }
          },
          username: {
            validators: {
              notEmpty: {
                message: '用户名不能为空',
              },
              stringLength: {
                min: 3,
                max: 10,
                message: '用户名必须大于3，小于10个字',
              }
            }
          },
          password: {
            stringLength: {
              min: 6,
              max: 15,
              message: '密码必须大于6，小于15个字'
            },
            regexp: {
              regexp: /^[a-zA-Z0-9_\.]+$/,
              message: '密码中含有特殊字符'
            }
          },
          cfmpassword: {
            validators: {
              identical: {
                field: 'password',
                message: '两次密码输入不一致',
              }
            }
          },
          tel: {
            validators: {
              notEmpty: {
                message: '手机号码不能为空',
              },
              regexp: {
                regexp: /^1[3|4|5|7|8]\d{9}$/,
                message: '请输入正确的手机号码格式',
              }
            }
          },
          intro: {
            validators: {
              stringLength: {
                max: 100,
                message: '个人简介必须小于100个字',
              }
            }
          }
        }
      })
      .on('success.form.bv', function(e) {
        e.preventDefault();
        if ($('#profile_form').data('bootstrapValidator').isValid()) {
          vm.update_profile();
          $location.url('/user_info/' + Authentication.getAuthenticatedAccount().user_info.id);
        }
      });
    }])
    .controller('actInfoCtrl', ['$scope', '$rootScope', '$route', '$location', '$routeParams', '$http', 'Authentication', function($scope, $rootScope, $route, $location, $routeParams, $http, Authentication){
      console.log('actInfo');
      $('#act_info_share').share();
      $http.get('/api/activity/detail/' + $routeParams.act_id).success(function(data) {
        $scope.act = data.act_info;
        console.log($scope.act);
        $http.get('/api/user/following').success(function(data) {
          console.log($scope.act);
          $scope.follow_list = data.following;
          console.log($scope.act.start_time);
          $scope.act.time = "[开始]: " + $scope.act.start_time + " - [结束]: " + $scope.act.end_time;
          $scope.F = function(user_id) {
            for (var i = 0; i < $scope.follow_list.length; i++) {
              if (user_id == $scope.follow_list[i].id) {
                return "取关";
              }
            }
            return "关注";
          }
          $scope.sendMsgTo = function(user) {
            $rootScope.getSendUser(user);
          }
          $scope.change_follow = function(user_id) {
            if ($scope.F(user_id) == "关注") {
              $http.post('/api/user/follow', $.param({'id': user_id})).success(function(data) {
                $scope.follow_list.push(user_id);
              })
            }
            else {
              $http.post('/api/user/unfollow', $.param({'id': user_id})).success(function(data) {
                $scope.follow_list.push(user_id);
              })
            }
          }
          $scope.allow_apply = function(user_id) {
            $http.post('/api/activity/reply_application', $.param({
              'act_id': $scope.act.id,
              'user_id': user_id,
              'reply': 1,
            })).success(function(data){
              console.log(data);
              $route.reload();
            });
          }
          $scope.deny_apply = function(user_id) {
            $http.post('/api/activity/reply_application', $.param({
              'act_id': $scope.act.id,
              'user_id': user_id,
              'reply': 0,
            })).success(function(data){
              console.log(data);
              $route.reload();
            });
          }
          $scope.promote = function(user_id) {
            $http.post('/api/activity/promote', $.param({
              'id': $scope.act.id,
              'user_id': user_id,
            })).success(function(data){
              console.log('promote')
              console.log(data);
              $route.reload();
            });
          }
          $scope.kick = function(user_id) {
            $http.post('/api/activity/kick', $.param({
              'id': $scope.act.id,
              'user_id': user_id,
            })).success(function(data){
              console.log(data);
              $route.reload();
            });
          }
          $scope.is_admin = function(user_id) {
            for (var i = 0; i < $scope.act.admins.length; i++) {
              if ($scope.act.admins[i].id == user_id) {
                return true;
              }
            }
            return false;
          }
          $('.follow-btn').click(function(){
            if ($(this).html() == "取关") {
              $(this).html("关注");
            }
            else {
              $(this).html("取关");
            }
          })
        });
        $scope.org_act = function() {
          if (Authentication.isAuthenticated()) {
            return Authentication.getAuthenticatedAccount().user_info.id == $scope.act.organizer.id;
          }
          else {
            return false;
          }
        }
        if (Authentication.isAuthenticated()) {
          $scope.login_user = Authentication.getAuthenticatedAccount().user_info;
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
      });
    }])
    .controller('userInfoCtrl', ['$http', '$rootScope', '$routeParams', '$scope', 'Authentication', function($http, $rootScope, $routeParams, $scope, Authentication) {
      $http.get('/api/user/detail/' + $routeParams.user_id).success(function(data) {
        $scope.user = data.user_info;
        console.log($scope.user);
      })
      $scope.apply_for = function(act_id) {
        $http.post('/api/user/apply', $.param({
          'act_id': act_id,
          'type': 1,
        }))
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
      $scope.sendMsgTo = function(user) {
        $rootScope.getSendUser(user);
      }
      $scope.overview = function() {
        $('.profile-tab').removeClass('active');
        $('#overview_tab').addClass('active');
        $('.sub_tab').css({'display': 'none'});
        $('#overview_sub_tab').css({'display': 'block'});
      }
      $scope.org_acts_view = function() {
        $('.profile-tab').removeClass('active');
        $('#org_acts_tab').addClass('active');
        $('.sub_tab').css({'display': 'none'});
        $('#org_acts_sub_tab').css({'display': 'block'});
      }
      $scope.join_acts_view = function() {
        $('.profile-tab').removeClass('active');
        $('#join_acts_tab').addClass('active');
        $('.sub_tab').css({'display': 'none'});
        $('#join_acts_sub_tab').css({'display': 'block'});
      }
      $scope.overview();
    }])
    .controller('activityCtrl', ['$route', '$http', '$location', '$scope', 'Authentication', function($route, $http, $location, $scope, Authentication){
      $(".act-nav").click(function(){
        $(".act-nav").not(this).removeClass("active");
        $(this).addClass("active");
      })
      $scope.myActs = function() {
        $scope.page_title = "组织的活动";
        $scope.act_type = "my_act";
        $('.act-nav').not('#myActs').removeClass("active");
        $('#myActs').addClass('active');
        $http.get('/api/user/get_admin_act').success(
          function(data){
            $scope.acts = data.admin_acts;
            console.log(data);
            $scope.acts.login_id = Authentication.getAuthenticatedAccount().user_info.id;
            console.log($scope.acts);
        });
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
        $scope.U = function(act) {
          if (act.state == 0) {
            $http.post('/api/activity/change_state', $.param({
              'id': act.id,
              'state': 1,
            })).success(function(){
              act.state = 1;
            });
          }
          else {
            $http.post('/api/activity/change_state', $.param({
              'id': act.id,
              'state': 0,
            })).success(function(){
              act.state = 0;
            });
          }
        }
        $scope.D = function(act) {
          $http.post('/api/activity/change_state', $.param({
            'id': act.id,
            'state': 2,
          })).success(function(){
            act.state = 2;
          });
        }
        $scope.T = function(state) {
          return {
            0: "接受报名",
            1: "结束报名",
            2: "已结束",
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
        $http.get('/api/user/get_join_act').success(
          function(data){
            console.log(data);
            $scope.join_acts = data.join_acts;
            $scope.apply_acts_member = data.apply_acts_member;
            $scope.apply_acts_admin = data.apply_acts_admin;
        });
        $scope.B = function(state) {
          return {
            0: "退出活动",
            1: "退出活动",
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
        $scope.Q = function(act) {
          $http.post('/api/user/quit_act', $.param({
            'act_id': act.id,
          })).success(function(data) {
            $route.reload();
          })
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
            'tags': $('#apply__tags').val(),
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
        $http.get('/api/user/recommend').success(
          function(data){
            console.log(data);
            $scope.acts = data.acts;
        });
        $scope.B = function(state) {
          return {
            0: "退出活动",
            1: "退出活动",
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
        $scope.Q = function(act) {
          $http.post('/api/user/quit_act', $.param({
            'act_id': act.id,
          })).success(function(data) {
            $route.reload();
          })
        }
      }
      $scope.myActs();

      //validator
      $scope.$on("$includeContentLoaded", function(event, templateName){
        $('#apply_form').bootstrapValidator({
          feedbackIcons: {
            valid: 'fa fa-check',
            invalid: 'fa fa-times',
            validating: 'fa fa-refresh'
          },
          fields: {
            name: {
              validators: {
                notEmpty: {
                  message: '活动名称不能为空'
                },
                stringLength: {
                  min: 2,
                  max: 10,
                  message: '活动名称必须大于2，小于10个字'
                }
              }
            },
            intro: {
              validators: {
                notEmpty: {
                  message: '活动简介不能为空'
                },
                stringLength: {
                  max: 1000,
                  message: '活动简介必须小于1000个字'
                }
              }
            },
            location: {
              validators: {
                notEmpty: {
                  message: '活动地点不能为空'
                },
                stringLength: {
                  max: 20,
                  message: '活动地点描述必须小于20个字'
                }
              }
            },
            cost: {
              validators: {
                notEmpty: {
                  message: '活动花费不能为空'
                },
                regexp: {
                  regexp: /^(([1-9]\d*)(\.\d{1,2})?)$|(0\.0?([1-9]\d?))$/,
                  message: '请填入正确的金额数目'
                }
              }
            }
          }
        })
        .on('success.form.bv', function(e) {
          e.preventDefault();
          if ($('#apply_form').data('bootstrapValidator').isValid()) {
            $scope.apply();
          }
        });
      });
    }])
    .controller('actProfileCtrl', ['$http', '$scope', '$location', '$routeParams', 'Authentication', function($http, $scope, $location, $routeParams, Authentication){
      $scope.week = CONST.WEEK;
      $scope.times = CONST.TIME_SEG;
      $scope.tags = "";

      $http.get('/api/activity/detail/' + $routeParams.act_id).success(function(data) {
        $scope.name = data.act_info.name;
        $scope.intro = data.act_info.intro;
        $scope.tags = data.act_info.tags.join(',');
        $scope.cost = data.act_info.cost;
        $scope.location = data.act_info.location;
        $.getScript('/static/lib/bootstrap-tagsinput/bootstrap-tagsinput.js');
      });

      //time picker
      $('#act_profile__date1').combodate({
        minYear: 2016,
        maxYear: 2026
      });
      $('#act_profile__date2').combodate({
        minYear: 2016,
        maxYear: 2026
      });

      //get recommend time
      $http.get('/api/activity/recommended_time/'+$routeParams.act_id).success(function(data) {
/*        data.result = [0.9, 0.8, 0, 0.6, 0.5, 1, 0.3,
                      1, 0.2, 0.3, 1, 0.5, 0.6, 0.01,
                      0.8, 0.1, 0.99, 1, 0.55, 0.65, 0.75,
                      1, 0.95, 1, 0.66, 1, 0.13, 0.45];*/
        var tds = $('#act_profile__fixed').find('td');
        for (var i = 0; i < 28; i++) {
          if ((data.result[i] >= 0) && (data.result[i] < 1)) {
            var green = parseInt(255 - data.result[i] * 128);
            tds[i].style.backgroundColor = 'rgba(0, '+green+', 0, '+(0.2+0.8*data.result[i])+')';
          }
        }
      });


      //submit
      $scope.save = function() {
        console.log($('#act_profile__tags').val());
        $http.post('/api/activity/update', $.param({
          'id': $routeParams.act_id,
          'name': $scope.name,
          'intro': $scope.intro,
          'tags': $('#act_profile__tags').val(),
          'cost': $scope.cost,
          'location': $scope.location,
          'time': $('#act_profile__date1').combodate('getValue', "YYYY-MM-DD HH"),
          'end_time': $('#act_profile__date2').combodate('getValue', "YYYY-MM-DD HH")
        })).success(function(data){
          console.log(data);
          $location.url('/act_info/' + $routeParams.act_id);
        });
      };

      //validator
      $('#act_profile_form').bootstrapValidator({
        feedbackIcons: {
          valid: 'fa fa-check',
          invalid: 'fa fa-times',
          validating: 'fa fa-refresh'
        },
        fields: {
          name: {
            validators: {
              notEmpty: {
                message: '活动名称不能为空'
              },
              stringLength: {
                min: 2,
                max: 10,
                message: '活动名称必须大于2，小于10个字'
              }
            }
          },
          intro: {
            validators: {
              notEmpty: {
                message: '活动简介不能为空'
              },
              stringLength: {
                max: 1000,
                message: '活动简介必须小于1000个字'
              }
            }
          },
          location: {
            validators: {
              notEmpty: {
                message: '活动地点不能为空'
              },
              stringLength: {
                max: 20,
                message: '活动地点描述必须小于20个字'
              }
            }
          },
          cost: {
            validators: {
              notEmpty: {
                message: '活动花费不能为空'
              },
              regexp: {
                regexp: /^(([0-9]\d*)(\.\d{1,2})?)$|(0\.0?([0-9]\d?))$/,
                message: '请填入正确的金额数目'
              }
            }
          }
        }
      })
      .on('success.form.bv', function(e) {
        e.preventDefault();
        if ($('#act_profile_form').data('bootstrapValidator').isValid()) {
          $scope.save();
        }
      });
    }])
    .controller('tagInfoCtrl', ['$http', '$rootScope', '$scope', '$routeParams', 'Authentication', function($http, $rootScope, $scope, $routeParams, Authentication){
      if (Authentication.isAuthenticated()) {
        $scope.login_user = Authentication.getAuthenticatedAccount().user_info;
      }
      $http.get('/api/tag/get/' + $routeParams.tag_name).success(function(data) {
        $scope.tag = $routeParams.tag_name;
        $scope.users = data.users;
        $scope.acts = data.acts;
        console.log(data);
        $http.get('/api/user/following').success(function(data) {
          console.log(data);
          $scope.follow_list = data.following;
          $scope.F = function(user_id) {
            for (var i = 0; i < $scope.follow_list.length; i++) {
              if (user_id == $scope.follow_list[i].id) {
                return "取关";
              }
            }
            return "关注";
          }
          $scope.sendMsgTo = function(user) {
            $rootScope.getSendUser(user);
          }
          $scope.change_follow = function(user_id) {
            if ($scope.F(user_id) == "关注") {
              $http.post('/api/user/follow', $.param({'id': user_id})).success(function(data) {
                $scope.follow_list.push(user_id);
              })
            }
            else {
              $http.post('/api/user/unfollow', $.param({'id': user_id})).success(function(data) {
                $scope.follow_list.push(user_id);
              })
            }
          }
          $('.follow-btn').click(function(){
            if ($(this).html() == "取关") {
              $(this).html("关注");
            }
            else {
              $(this).html("取关");
            }
          })
        })
      });
    }])
    .controller('followInfoCtrl', ['$http', '$scope', '$rootScope', '$routeParams', 'Authentication', function($http, $scope, $rootScope, $routeParams, Authentication){
      if (Authentication.isAuthenticated()) {
        $scope.login_user = Authentication.getAuthenticatedAccount().user_info;
      }
      $http.get('/api/user/following').success(function(data) {
        $scope.following = data.following;
        console.log(data);
        $scope.F1 = function(user_id) {
          for (var i = 0; i < $scope.following.length; i++) {
            if (user_id == $scope.following[i].id) {
              return "取关";
            }
          }
          return "关注";
        }
        $scope.sendMsgTo = function(user) {
          $rootScope.getSendUser(user);
        }
        $scope.change_following = function(user_id, user_name) {
          if ($scope.F1(user_id) == "关注") {
            $http.post('/api/user/follow', $.param({'id': user_id})).success(function(data) {
              $scope.following.push({'id': user_id, 'name': user_name});
            })
          }
          else {
            $http.post('/api/user/unfollow', $.param({'id': user_id})).success(function(data) {
              var tmp = [];
              for (var i = 0; i < $scope.following.length; i++) {
                if ($scope.following[i].id != user_id) {
                  tmp.push({'id': $scope.following[i].id, 'name': $scope.following[i].name})
                }
              }
              console.log(tmp);
              $scope.following = tmp;
            })
          }
        }
        $http.get('/api/user/follower').success(function(data) {
          console.log(data);
          $scope.follower = data.follower;
        })
      });
    }])
    .controller('msgBoxCtrl', ['$http', '$sce', '$scope', '$rootScope', 'Authentication', function($http, $sce, $scope, $rootScope, Authentication) {
      var round_robin = function() {
        $scope.timer = setInterval(function(){
          $http.post('/api/user/message/get', $.param({
            'id': Authentication.getAuthenticatedAccount().user_info.id,
          })).success(function(data){
//            console.log(data);
            for (var i = 0; i < data.messages.length; i++) {
              if (data.messages[i].content[0] == '0' && data.messages[i].read == false && data.messages[i].to == Authentication.getAuthenticatedAccount().user_info.id) {
                //message_list.push("来自@" + data.messages[i].from + ": " + data.messages[i].content.slice(3));
                $scope.msgs.push($sce.trustAsHtml("来自@<a href='/user_info/" + data.messages[i].from_id + "'>" + data.messages[i].from + "</a>: " + data.messages[i].content.slice(3)));
                $http.get('/api/user/message/set_state/' + data.messages[i].id + '/1').success(function(data){
                  console.log(data);
                });
              }else
              if (data.messages[i].content[0] == '1' && data.messages[i].read == false) {
              }
            }
          })
        }, 2000);
      }
      var kill_robin = function() {
        if ($scope.timer) {
          clearInterval($scope.timer);
        }
      }
      $('#message-box').click(function(){
        if ($('#message-list').css('opacity') == 0) {
          $('#message-list').css({'display': 'block'}).animate({'opacity': 1}, 100);
        }
        else {
          $('#message-list').animate({'opacity': 0}, 100).css({'display': 'none'});
        }
      });
      $rootScope.getSendUser = function(user){
        $scope.msg_content = user.name + ":";
        $rootScope.send_to_user = user;
        $('#message-list').css({'display': 'block'}).animate({'opacity': 1}, 100);
      }
      $rootScope.writeMsg = function(msg) {
        $('#message-list').css({'display': 'block'}).animate({'opacity': 1}, 100);
      }
      $scope.send_message = function() {
        console.log($scope.msg_content);
        var msg = $scope.msg_content.slice($scope.msg_content.indexOf(':') + 1);
        if (msg) {
          $http.post('/api/user/message/send', $.param({
            'id': $rootScope.send_to_user.id,
            'content': msg,
          })).success(function(){
            $scope.msg_content = '';
          });
        }
      }
      $scope.msgs = [];
      $scope.send_content = "";
      if (Authentication.isAuthenticated()) {
        $('#message-box').css({'display': 'block'});
        $('#message-list').css({'opacity': 0}).css({'display': 'none'});
        round_robin();
      }
      else {
        $('#message-box').css({'display': 'none'});
        $('#message-list').css({'opacity': 0}).css({'display': 'none'});
      }
      $rootScope.$on('login_done', function(){
        $('#message-box').css({'display': 'block'});
        $('#message-list').css({'opacity': 0}).css({'display': 'none'});
        round_robin();
      });
      $rootScope.$on('logout_done', function(){
        $('#message-box').css({'display': 'none'});
        $('#message-list').css({'opacity': 0}).css({'display': 'none'});
        kill_robin();
      });
    }])
    .controller('navbarCtrl', ['$location', '$http', '$scope', '$rootScope', 'Authentication', function($location, $http, $scope, $rootScope, Authentication){
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
        $location.url('/follow_info');
      }
      $scope.register = register;
      if (Authentication.isAuthenticated()) {
        $scope.displayName = Authentication.getAuthenticatedAccount().user_info.name;
        $scope.login_id = Authentication.getAuthenticatedAccount().user_info.id;
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
        $scope.login_id = Authentication.getAuthenticatedAccount().user_info.id;
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
