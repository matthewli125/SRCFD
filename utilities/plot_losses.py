import matplotlib.pyplot as plt
import re

with open("loss_latest.txt") as file:
    lines = file.readlines()

print(len(lines))
print(re.search(r"loss = \[\d+\.\d+(e-\d+)?",lines[274]).group(0).split("[")[1])

discriminator_losses = [float(re.search(r"discriminator_loss = \d+\.\d+",i).group(0).split("= ")[1]) for i in lines]
generator_losses = [float(re.search(r"loss = \[\d+\.\d+(e-\d+)?",i).group(0).split("[")[1]) for i in lines]
x = [i for i in range(1,len(lines)+1)]

fig,ax =plt.subplots(nrows=1,ncols=2,figsize=(14,5))
ax[0].plot(x,discriminator_losses)
ax[0].set_title("discriminator loss")
ax[0].set_ylim([0, 0.5])
ax[1].plot(x,generator_losses,color="orange")
ax[1].set_title("generator loss")
plt.show()
