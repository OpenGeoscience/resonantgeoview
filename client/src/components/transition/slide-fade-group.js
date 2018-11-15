import Vue from 'vue';

export default Vue.component('slide-fade-group', {
  functional: true,
  render: function (createElement, context) {
    var data = {
      staticClass: context.data.staticClass,
      props: {
        name: 'slide-fade-group',
        tag: context.props.tag
      },
      on: {
        beforeLeave(el) {
          var parent = el.parentElement;
          if (
            !(
              parent.scrollHeight > parent.clientHeight ||
              parent.scrollWidth > parent.clientWidth
            )
          ) {
            parent.style.overflowY = "hidden";
          }
          el._parentElement = parent;
        },
        afterLeave(el) {
          el._parentElement.style.overflowY = null;
        }
      }
    }
    return createElement('transition-group', data, context.children)
  }
});
