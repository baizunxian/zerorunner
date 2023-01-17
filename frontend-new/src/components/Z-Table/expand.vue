<script lang="ts">
import {defineComponent, VNodeChild} from 'vue'

type IProp = {
  render: (row: Record<string, any>, index: number) => VNodeChild
  row: Record<string, any>
  index: number
}
export default defineComponent({
  props: {
    row: Object,
    render: Function,
    index: Number
  },
  setup(props: IProp) {
    return () => props.render && props.render(props.row, props.index)
  }
})
</script>
