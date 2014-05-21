(function(window, angular) {
  'use strict';

  var combos = angular.module('gdlk.combos');

  combos.controller('DetailsController', function($scope, $stateParams, Combo) {
    Combo.get(1).then(function(combo) {
      $scope.combo = combo;
    });
  });

})(window, window.angular);
