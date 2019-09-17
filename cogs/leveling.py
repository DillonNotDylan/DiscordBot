# tracking joining members
@client.event
async def on_member_join(member):
    print(f"{member} has joined the chat!")
    with open('members.json', 'r') as f:
        members = json.load(f)

    await update_data(members, member)

    with open('members.json', 'w') as f:
        json.dump(members, f)

# tracking messages
@client.event
async def on_message(self, message):
    if message.author == self.bot.users:
        return

    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    await client.process_commands(message)

    with open('members.json', 'r') as f:
        members = json.load(f)

    await update_data(members, message.author)
    await add_xp(members, message.author, 100)
    await level_up(members, message.author, message.channel)

    with open('members.json', 'w') as f:
        json.dump(members, f)

async def update_data(members, member):
    if not member.id in members:
        members[member.id] = {}
        members[member.id]['experience'] = 0
        members[member.id]['level'] = 1

async def add_xp(members, member, xp):
    members[member.id]['experience'] += xp

async def level_up(members, member, channel):
    experience = members[member.id]['experience']
    current_level = members[member.id]['level']
    next_level = int(experience ** (1/4))

    if current_level < next_level:
        await ctx.send(channel, '{} has leveled up to level {}'.format(member.mention, next_level))
        members[member.id]['level'] = next_level
