from math import exp,log

#
# helper functions - nothing to see here
#

def intersect(l1, l2):
	return list(set(l1) & set(l2))

def myLog (n):
	if n == 0:
		return -9999999999999
	else:
		return log(n)

#
# parameters
#

#prior = [.25,.25,.25,.25]
	# define globally for use in both L0 and L1

## OTHER PRIORS:
#prior = [.3,.2,.3,.2] # Obama worries about coming off as aloof
prior = [.2,.2,.3,.3] # Obama worries about coming off as incompetent



#
# interesting functions vis-a-vis model
# 

properties = ['competent','incompetent','friendly','aloof']
personae = [
	['competent','aloof'],
	['competent','friendly'],
	['incompetent','aloof'],
	['incompetent','friendly']
] 

messages = ['in','ing']

def field (m):
	if m == 'ing':
		return ['competent','aloof']
	elif m == 'in':
		return ['incompetent','friendly']

def em_field (m):
	return [p for p in personae if len(intersect(p, field(m))) != 0]

def update(prior, lik):
	# prior, lik should be equal-length lists of numbers
	# prior should sum to 1
	post_NN = [p * l for (p,l) in zip(prior, lik)]
	NC = sum(post_NN)
	return [p/NC for p in post_NN]

def listener0 (m):
	lik = [1 if p in em_field(m) else 0 for p in personae]
	posterior = update(prior, lik)
	r = dict()
	for p in personae:
		r[','.join(p)] = posterior[personae.index(p)]
	return r

l0_message_effects = dict()
for m in messages:
	l0_message_effects[m] = listener0(m)

def speaker1 (persona, alpha):
	# no message costs in this version
	utilities = [myLog(l0_message_effects[m][','.join(persona)]) for m in messages]
	production_NN = [exp(alpha * u) for u in utilities]
	NC = sum(production_NN)
	posterior = [p/NC for p in production_NN]
	r = dict()
	for m in messages:
		r[m] = posterior[messages.index(m)]
	return r 

def listener1 (m, alpha):
	lik = [speaker1(p, alpha)[m] for p in personae]
	posterior = update(prior, lik)
	r = dict()
	for p in personae:
		r[','.join(p)] = posterior[personae.index(p)]
	return r

l1_message_effects = dict()
for m in messages:
	l1_message_effects[m] = listener1(m, alpha=6)

#
# Obama wants to be the cool guy. Alpha = 6.
#
print '\n'
print speaker1 (['competent','friendly'], 6)
print '\n'

#
#Obama wants to be the stern leader. Alpha = 6.
#
print speaker1 (['competent','aloof'], 6)


#
# print listener results
#

print '\n'
for m in messages:
	interp = l1_message_effects[m]
	print 'Message: "%s"' %m
	for p in personae:
		nm = ','.join(p)
		print '\t%s: %s'%(nm, round(interp[nm],2))
print '\n'

