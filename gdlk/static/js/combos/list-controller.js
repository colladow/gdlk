(function(window, angular) {
  'use strict';

  var combos = angular.module('gdlk.combos');

  combos.controller('ListController', function($scope, Combo) {
    Combo.query().then(function(response) {
      $scope.combos = response.data;
    });;
  });

})(window, window.angular);
