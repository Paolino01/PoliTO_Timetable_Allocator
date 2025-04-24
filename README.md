# PoliTO_Timetable_Allocator

Allocator for PoliTO courses timetable

> TODO: the final version of the software will have full documentation

The allocator implements the following constraints, divided in hard constraints (which should always be respected) and soft constraints (which should be maximized):

### Hard Constraints

#### Teachings:

- Slots per week: each Teaching must have the exact amount of Lectures, Practices and Lab Slots per week, based on the total number of hours for the Teaching in the Semester
- Number of consecutive Slots: each Teaching must have at most 2 Slots in a Day and, if so, the two Slots must be consecutive. We should also consider the Teacher's preferences about the consecutive Slots for a Teaching, but at the moment we do not consider that because otherwise it would not be possible to find a solution
- Limited number of Teachings in a Day: the number of "correlated" Teachings in a Day is limited (<= 500, at the moment), in order to not have too many consecutive lectures in the same Day
- Overlaps:
    - Teachings with a correlation > 20 must not overlap
    - The same Groups of Practice Lectures of different Teachings with a correlation > 20 can not overlap (e.g. Practice Group1 of TeachingA can not overlap with Practice Group1 of TeachingB, but Practice Group1 of TeachingA CAN overlap with Practice Group2 of TeachingB
    - The same Groups of Lab Lectures of different Teachings with a correlation > 20 can not overlap (e.g. Lab Group1 of TeachingA can not overlap with Lab Group1 of TeachingB, but Lab Group1 of TeachingA CAN overlap with Lab Group2 of TeachingB
- Correlation between consecutive Slots: the number of correlated Teachings in consecutive Slots should be above a certain treshold (80, at the moment), in order to not have too many empty Slots in a Day
- Correlation between first and last Slot of Day: the sum of the correlation of Teachings in the first and last Slots of the Day must be under a treshold (20, at the moment), in orded to not have lectures at 8:30 and at 17:30

#### Teachers:

- Overlaps: Teachings taught by the same Teacher must not overlap (considering Lectures, Practices, and Labs)
- Unavailable Slots: each Teracher can indicate up to 4 Slots in which they are unavailable. Their Teachings cannot be allocated in those Slots
- Consecutive Lectures: each Teacher can not have more than 2 consecutive Slots

### Soft Constraints

- Difference between the first and last lecture of a Day: the difference between the first lecture Slot of a Day and the last one should be minimized (while mantaining some empty Slots during the Day), in order to have a more compact timetable
- Overlaps: the overlaps between Teachings with a correlation <= 20 should be minimized
