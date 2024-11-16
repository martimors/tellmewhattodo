import { describe, it, expect } from 'vitest'

import { mount } from '@vue/test-utils'
import AlertItem from '../AlertItem.vue'

describe('HelloWorld', () => {
  it('renders properly', () => {
    const wrapper = mount(AlertItem, { props: { name: 'Hello Vitest' } })
    expect(wrapper.text()).toContain('Hello Vitest')
  })
})
