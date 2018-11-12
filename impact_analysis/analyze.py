from matplotlib import pyplot as plt
from numpy import arange


from impact_analysis.prepare_data import prepare_data

d_frame = prepare_data('../data/final/result.json', '../data/final/Repo_Commits_JSON.json')

plt.figure()
plt.xlabel('Follows commit rule')
plt.ylabel('Success index')
plt.xticks(arange(2), ['False', 'True'])
plt.scatter(list(d_frame['isConform']), list(d_frame['successIndex']), c=list(d_frame['successIndex']), cmap='plasma')
plt.savefig('scatterSuccessConformity.png', dpi=400)
plt.show()

print('\n\n')
print('Analysis:\n')

conform_frame = d_frame[d_frame['isConform']]
conform_count = len(conform_frame.index)

not_conform_frame = d_frame[~ d_frame['isConform']]
not_conform_count = len(not_conform_frame.index)

complete_count = len(d_frame.index)

print('Total data size:' + str(complete_count))
print('Conform percent: ' + str(conform_count * 100 / complete_count) + '%')
print('Not conform percent: ' + str(not_conform_count * 100 / complete_count) + '%')
print('Is exact computation: ' + str(conform_count + not_conform_count == complete_count))


plt.figure()
d_frame.boxplot(column=['successIndex'], by='isConform')
plt.show()
