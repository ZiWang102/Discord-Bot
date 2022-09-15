from hashlib import new
import discord
import random
import os
import time
import bloobot_classes
import bloobot_method
from dotenv import load_dotenv
load_dotenv()
bloobot = discord.Bot()

characters = {}

resume = {}

@bloobot.event
async def on_ready() :
    print(f"Bloo is primed and ready")

@bloobot.slash_command(name = "hello", description = "Say hello to Bloo")
async def hello(ctx):
    embed = discord.Embed(
        title="Hello c:",
        color=discord.Colour.blurple()
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/986250722205114401/996396783557161051/Bee_Happy_Emote.png")
    await ctx.respond("",embed=embed)

@bloobot.slash_command(name = "multiply", description = "Multiplies two numbers")
async def mult(ctx, number1, number2):
    sum = float(number1)*float(number2)
    await ctx.respond(f"Multiplication = {sum}")

@bloobot.slash_command(name = "divide", description = "Divides two numbers")
async def div(ctx, number1, number2):
    sum = float(number1)/float(number2)
    await ctx.respond(f"Division = {sum}")

@bloobot.slash_command(name = "stats", description = "Shows stats of your character")
async def stats(ctx):
    embed = discord.Embed(
        title=(f"{ctx.author.name}'s character"),
        description=(f"Class: {characters[ctx.author.id].f_class}\nLevel = {characters[ctx.author.id].level}\nCurrent HP:{characters[ctx.author.id].current_hp}\nGold: {characters[ctx.author.id].money}"),
        color=discord.Colour.blurple(),
    )
    embed.add_field(name="Stats",value = (f"Max HP = {characters[ctx.author.id].max_hp}\nINT = {characters[ctx.author.id].int}\nSTR = {characters[ctx.author.id].str}\nDEX = {characters[ctx.author.id].dex}"))
    embed.add_field(name="Skills", value = (f"Attack Skill: {characters[ctx.author.id].attack_skill}\nSpecial Skill: {characters[ctx.author.id].special_skill}"))
    await ctx.respond("",embed=embed)

@bloobot.slash_command(name = "adventure", description = "continue where you left off")
async def adventure(ctx):
    backer = resume[ctx.author.id]
    if backer == "View":
        embed = discord.Embed(
        title="Beginning",
        description="You wake up in an stange and unfamiliar bedroom, you don't remember what happend. You can't seem to understand why you are there or even who you are. All you know is that you feel a connection with something far beyond. All of a sudden, you hear footsteps approaching from outside.\n*Thump* *Thump* *Thump*\nLoud knocks come from downstairs.\n*Boom* *Boom*\nWhat do you do?\n(Do /adventure to continue)",
        color=discord.Colour.blurple()
        )
        view_var = View(ctx)
        await ctx.respond("", view=view_var, embed = embed)
    elif backer == "Pick":
        next_view = Pick(ctx)
        embed = discord.Embed(
        description="\"Greetings Brave Soul\" the man says, \"Would you like to join the Adventurer's Guild?\"\nYou nod as he pulls out a piece of paper\nHe then asks \"What is your class?\"",
        color=discord.Colour.blurple()
        )
        await ctx.respond("",view=next_view,embed = embed)
    elif backer == "ChooseArea":
        next_view = ChooseArea(ctx)
        embed1 = discord.Embed(
        description="Where would you like to adventure?",
        color=discord.Colour.blurple()
        )
        await ctx.respond("",view=next_view,embed=embed1)
    elif backer == "Action":
        pick_view = Actions(ctx)
        embed = discord.Embed(
        description="You arrive in the forest what would you like to do?",
        color=discord.Colour.blurple()
        )
        await ctx.respond("",view=pick_view,embed=embed)
    elif backer == "Targetting":
        target_view = Targetting(ctx)
        embed = discord.Embed(
        description=f"Enemy List",
        color=discord.Colour.blurple()
        )
        for mobs in characters[ctx.author.id].mob_data:
            embed.add_field(name=mobs.species, value=f"HP: {mobs.current_hp}")
        await ctx.respond("", view=target_view, embed = embed)        

class Targetting(discord.ui.View):
    def __init__(self, ctx):
        self.ctx = ctx
        super().__init__()
        
    @discord.ui.button(label="Attack Skill", style=discord.ButtonStyle.red)
    async def button_callback1(self, button, interaction):
        self.children[0].disabled = True
        if len(characters[self.ctx.author.id].mob_data) >= 1 and characters[self.ctx.author.id].mob_data[0].species != "dead":
            self.children[2].disabled = False
        if len(characters[self.ctx.author.id].mob_data) >= 2 and characters[self.ctx.author.id].mob_data[1].species != "dead":
            self.children[3].disabled = False
        if len(characters[self.ctx.author.id].mob_data) >= 3 and characters[self.ctx.author.id].mob_data[2].species != "dead":
            self.children[4].disabled = False
        if len(characters[self.ctx.author.id].mob_data) >= 4 and characters[self.ctx.author.id].mob_data[3].species != "dead":
            self.children[5].disabled = False
        await interaction.response.edit_message(view=self)
    
    @discord.ui.button(label="Special Skill", style=discord.ButtonStyle.gray)
    async def button_callback2(self, button, interaction):
        if characters[self.ctx.author.id].buffs == "":
            for child in self.children:
                child.disabled = True
            await interaction.response.edit_message(view=self)
        else:
            self.children[1].disabled = True
            button.label = "Already Buffed"
    
    @discord.ui.button(label="Enemy 1", style=discord.ButtonStyle.red,disabled=True)
    async def button_callback3(self, button, interaction):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)
        damage = bloobot_method.primary_attacks(characters[self.ctx.author.id])
        if characters[self.ctx.author.id].mob_data[0].current_hp - damage > 1:
            characters[self.ctx.author.id].mob_data[0].current_hp = characters[self.ctx.author.id].mob_data[0].current_hp - damage
            embed_char = discord.Embed(
            description=f"You delt {damage} damage to the {characters[self.ctx.author.id].mob_data[0].species}",
            color=discord.Colour.blurple()
            )
            await self.ctx.respond("",embed=embed_char)
        else: 
            embed_death = discord.Embed(
            description=f"You dealt {damage} damage to the {characters[self.ctx.author.id].mob_data[0].species}\nThe {characters[self.ctx.author.id].mob_data[0].species} has died",
            color=discord.Colour.blurple()
            )
            await self.ctx.respond("",embed=embed_death)
            characters[self.ctx.author.id].mob_data.pop(0)
        if len(characters[self.ctx.author.id].mob_data) == 0:
            embed = discord.Embed(
            description="You have defeated all the enemies\nDo /adventure to continue",
            color=discord.Colour.blurple()
            )
            resume[self.ctx.author.id] = "Action"
            await self.ctx.respond("",embed=embed)
        else:
            for mobs in characters[self.ctx.author.id].mob_data:
                mob_damage = bloobot_method.primary_attacks(mobs)
                if characters[self.ctx.author.id].current_hp - mob_damage < 1:
                    embed_player_death = discord.Embed(
                    description=f"You have died\n Please use /begin to start a new journey",
                    color=discord.Colour.blurple()
                    )
                    await self.ctx.respond("",embed=embed_player_death)
                    resume[self.ctx.author.id] = "None"
                    break
                else:
                    characters[self.ctx.author.id].current_hp = characters[self.ctx.author.id].current_hp - mob_damage
                embed_mawb = discord.Embed(
                description=f"{mobs.species} dealt {mob_damage} damage to you\nYou are now at {characters[self.ctx.author.id].current_hp} hp",
                color=discord.Colour.blurple()
                )
                await self.ctx.respond("",embed=embed_mawb)
            if resume[self.ctx.author.id] != "None":
                embed = discord.Embed(
                description=f"Enemy List",
                color=discord.Colour.blurple()
                )
                for mobs in characters[self.ctx.author.id].mob_data:
                    embed.add_field(name=mobs.species, value=f"HP: {mobs.current_hp}")
                resume[self.ctx.author.id] = "Fight"
                await self.ctx.respond("",embed=embed)

    @discord.ui.button(label="Enemy 2", style=discord.ButtonStyle.red,disabled=True)
    async def button_callback4(self, button, interaction):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)
        damage = bloobot_method.primary_attacks(characters[self.ctx.author.id])
        if characters[self.ctx.author.id].mob_data[1].current_hp - damage > 1:
            characters[self.ctx.author.id].mob_data[1].current_hp = characters[self.ctx.author.id].mob_data[1].current_hp - damage
        else: 
            characters[self.ctx.author.id].mob_data[1].current_hp = 0
            characters[self.ctx.author.id].mob_data.pop(1)
            embed_death = discord.Embed(
            description=f"You dealt {damage} damage to the {characters[self.ctx.author.id].mob_data[1].species}\nThe {characters[self.ctx.author.id].mob_data[1].species} has died",
            color=discord.Colour.blurple()
            )
            await self.ctx.respond("",embed=embed_death)
        for mobs in characters[self.ctx.author.id].mob_data:
            mob_damage = bloobot_method.primary_attacks(mobs)
            if characters[self.ctx.author.id].current_hp - mob_damage < 1:
                    embed_player_death = discord.Embed(
                    description=f"You have died\n Please use /begin to start a new journey",
                    color=discord.Colour.blurple()
                    )
                    await self.ctx.respond("",embed=embed_player_death)
                    resume[self.ctx.author.id] = "None"
                    break
            else:
                characters[self.ctx.author.id].current_hp = characters[self.ctx.author.id].current_hp - mob_damage
            embed_mawb = discord.Embed(
            description=f"{mobs.species} dealt {mob_damage} damage to you\nYou are now at {characters[self.ctx.author.id].current_hp} hp",
            color=discord.Colour.blurple()
            )
            await self.ctx.respond("",embed=embed_mawb)
        if resume[self.ctx.author.id] != "None":
            embed = discord.Embed(
            description=f"Enemy List",
            color=discord.Colour.blurple()
            )
            for mobs in characters[self.ctx.author.id].mob_data:
                embed.add_field(name=mobs.species, value=f"HP: {mobs.current_hp}")
            resume[self.ctx.author.id] = "Fight"
            await self.ctx.respond("",embed=embed)
        
    @discord.ui.button(label="Enemy 3", style=discord.ButtonStyle.red,disabled=True)
    async def button_callback5(self, button, interaction):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)
        damage = bloobot_method.primary_attacks(characters[self.ctx.author.id])
        if characters[self.ctx.author.id].mob_data[2].current_hp - damage > 1:
            characters[self.ctx.author.id].mob_data[2].current_hp = characters[self.ctx.author.id].mob_data[2].current_hp - damage
        else: 
            characters[self.ctx.author.id].mob_data[2].current_hp = 0
            characters[self.ctx.author.id].mob_data.pop(2)
            embed_death = discord.Embed(
            description=f"You dealt {damage} damage to the {characters[self.ctx.author.id].mob_data[2].species}\nThe {characters[self.ctx.author.id].mob_data[2].species} has died",
            color=discord.Colour.blurple()
            )
            await self.ctx.respond("",embed=embed_death)
        for mobs in characters[self.ctx.author.id].mob_data:
            mob_damage = bloobot_method.primary_attacks(mobs)
            if characters[self.ctx.author.id].current_hp - mob_damage < 1:
                    embed_player_death = discord.Embed(
                    description=f"You have died\n Please use /begin to start a new journey",
                    color=discord.Colour.blurple()
                    )
                    await self.ctx.respond("",embed=embed_player_death)
                    resume[self.ctx.author.id] = "None"
                    break
            else:
                characters[self.ctx.author.id].current_hp = characters[self.ctx.author.id].current_hp - mob_damage
            embed_mawb = discord.Embed(
            description=f"{mobs.species} dealt {mob_damage} damage to you\nYou are now at {characters[self.ctx.author.id].current_hp} hp",
            color=discord.Colour.blurple()
            )
            await self.ctx.respond("",embed=embed_mawb)
        if resume[self.ctx.author.id] != "None":
            embed = discord.Embed(
            description=f"Enemy List",
            color=discord.Colour.blurple()
            )
            for mobs in characters[self.ctx.author.id].mob_data:
                embed.add_field(name=mobs.species, value=f"HP: {mobs.current_hp}")
            resume[self.ctx.author.id] = "Fight"
            await self.ctx.respond("",embed=embed)

    @discord.ui.button(label="Enemy 4", style=discord.ButtonStyle.red,disabled=True)
    async def button_callback6(self, button, interaction):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)
        damage = bloobot_method.primary_attacks(characters[self.ctx.author.id])
        if characters[self.ctx.author.id].mob_data[3].current_hp - damage > 1:
            characters[self.ctx.author.id].mob_data[3].current_hp = characters[self.ctx.author.id].mob_data[3].current_hp - damage
        else: 
            characters[self.ctx.author.id].mob_data[3].current_hp = 0
            characters[self.ctx.author.id].mob_data.pop(3)
            embed_death = discord.Embed(
            description=f"You dealt {damage} damage to the {characters[self.ctx.author.id].mob_data[3].species}\nThe {characters[self.ctx.author.id].mob_data[3].species} has died",
            color=discord.Colour.blurple()
            )
            await self.ctx.respond("",embed=embed_death)
        for mobs in characters[self.ctx.author.id].mob_data:
            mob_damage = bloobot_method.primary_attacks(mobs)
            if characters[self.ctx.author.id].current_hp - mob_damage < 1:
                    embed_player_death = discord.Embed(
                    description=f"You have died\n Please use /begin to start a new journey",
                    color=discord.Colour.blurple()
                    )
                    await self.ctx.respond("",embed=embed_player_death)
                    resume[self.ctx.author.id] = "None"
                    break
            else:
                characters[self.ctx.author.id].current_hp = characters[self.ctx.author.id].current_hp - mob_damage
            embed_mawb = discord.Embed(
            description=f"{mobs.species} dealt {mob_damage} damage to you\nYou are now at {characters[self.ctx.author.id].current_hp} hp",
            color=discord.Colour.blurple()
            )
            await self.ctx.respond("",embed=embed_mawb)
        if resume[self.ctx.author.id] != "None":
            embed = discord.Embed(
            description=f"Enemy List",
            color=discord.Colour.blurple()
            )
            for mobs in characters[self.ctx.author.id].mob_data:
                embed.add_field(name=mobs.species, value=f"HP: {mobs.current_hp}")
            resume[self.ctx.author.id] = "Fight"
            await self.ctx.respond("",embed=embed)

class Actions(discord.ui.View):
    def __init__(self, ctx):
        self.ctx = ctx
        super().__init__()

    @discord.ui.button(label="Search Around", style=discord.ButtonStyle.blurple, emoji="🔎")
    async def button_callback1(self, button, interaction):
        #70% chance to encounter mob
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)
        outcome = random.randint(0,9)
        if outcome == 0 or outcome == 1 or outcome == 2 or outcome == 3 or outcome == 4 or outcome == 5 or outcome == 6:
            #chooses what mob it comes out to ************* Changing to only gobling right now 
            mob_select = 0
            #Spawns Goblins
            if mob_select == 0:
                numb_mob = random.randint(1,3)
                for x in range(numb_mob):
                    characters[self.ctx.author.id].mob_data.append(bloobot_method.create_mob('goblin'))
                resume[self.ctx.author.id] = "Targetting"
                embed = discord.Embed(
                description=f"You encounter {len(characters[self.ctx.author.id].mob_data)} {characters[self.ctx.author.id].mob_data[0].species}s",
                color=discord.Colour.blurple()
                )
                await self.ctx.respond("",embed=embed)
            #Spawns Trents
            elif mob_select == 1:
                numb_mob = random.randint(1,2)
                for x in range(numb_mob):
                    characters[self.ctx.author.id].mob_data.append(bloobot_method.create_mob('trent'))
                resume[self.ctx.author.id] = "Targetting"
                embed = discord.Embed(
                description=f"You encounter {len(characters[self.ctx.author.id].mob_data)} {characters[self.ctx.author.id].mob_data[0].species}s",
                color=discord.Colour.blurple()
                )
                await self.ctx.respond("",embed=embed)
            #Spawns Wolves
            elif mob_select == 2:
                numb_mob = random.randint(1,4)
                for x in range(numb_mob):
                    characters[self.ctx.author.id].mob_data.append(bloobot_method.create_mob('wolf'))
                resume[self.ctx.author.id] = "Targetting"
                embed = discord.Embed(
                description=f"You encounter {len(characters[self.ctx.author.id].mob_data)} {characters[self.ctx.author.id].mob_data[0].species}s",
                color=discord.Colour.blurple()
                )
                await self.ctx.respond("",embed=embed)
            #Spawns an Orge
            elif mob_select == 3:
                characters[self.ctx.author.id].mob_data.append(bloobot_method.create_mob('orge'))
                resume[self.ctx.author.id] = "Targetting"
                embed = discord.Embed(
                description=f"You encounter {len(characters[self.ctx.author.id].mob_data)} {characters[self.ctx.author.id].mob_data[0].species}s",
                color=discord.Colour.blurple()
                )
                await self.ctx.respond("",embed=embed)
        #10% chance to obtain gold
        elif outcome == 7:
            gold = random.randint(1,100)
            characters[self.ctx.author.id].money
            #put getting gold text
            embed = discord.Embed(
            description=f"You find {gold} gold pieces",
            color=discord.Colour.blurple()
            )
            await self.ctx.respond("",embed=embed)
            #sends player back to the action screen
            resume[self.ctx.author.id] = "Action"
        #20% chance for a unique encounter
        elif outcome == 8 or outcome == 9: 
            embed = discord.Embed(
            description="Place holder",
            color=discord.Colour.blurple()
            )
            await self.ctx.respond("",embed=embed)

    @discord.ui.button(label="Fish", style=discord.ButtonStyle.blurple, emoji="🚶‍♂️")
    async def button_callback2(self, button, interaction):
        await self.ctx.respond.send_message("Among Us")

    @discord.ui.button(label="Go to town", style=discord.ButtonStyle.blurple, emoji="🚶‍♂️")
    async def button_callback3(self, button, interaction):
        await self.ctx.respond.send_message("Among Us")

    @discord.ui.button(label="Summon Boss", style=discord.ButtonStyle.blurple, emoji="💀")
    async def button_callback4(self, button, interaction):
        await self.ctx.response.send_message("Among Us")


    async def interaction_check(self, interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("You are not allowed to interact with this",ephemeral=1)
            return False
        else:
            return True

class ChooseArea(discord.ui.View):

    def __init__(self, ctx):
        self.ctx = ctx
        super().__init__()
    
    @discord.ui.button(label="Forests", style=discord.ButtonStyle.blurple, emoji="🌳")
    async def button_callback1(self, button, interaction):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)
        embed = discord.Embed(
        description="You head towards the forests.",
        color=discord.Colour.blurple()
        )
        resume[self.ctx.author.id] = "Action"
        await self.ctx.respond("",embed=embed)

    async def interaction_check(self, interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("You are not allowed to interact with this",ephemeral=1)
            return False
        else:
            return True

class Pick(discord.ui.View):

    def __init__(self, ctx):
        self.ctx = ctx
        super().__init__()

    @discord.ui.button(label="Warrior", style=discord.ButtonStyle.blurple, emoji="⚔️")
    async def button_callback1(self, button, interaction):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)
        new_char = bloobot_classes.Character()
        new_char.current_hp = 20
        new_char.max_hp = 20
        new_char.int = 5
        new_char.str = 20
        new_char.dex = 5
        new_char.money = 80
        new_char.attack_skill = "Slash Strike"
        new_char.special_skill = "Shield Block"
        new_char.f_class = "Warrior"
        characters[self.ctx.author.id] = new_char
        embed = discord.Embed(
        description="So You Are a Mighty Warrior,\nYour combat prowess will be useful in the upcoming fight",
        color=discord.Colour.blurple()
        )
        resume[self.ctx.author.id] = "ChooseArea"
        await self.ctx.respond("",embed=embed)
    
    @discord.ui.button(label="Priest", style=discord.ButtonStyle.blurple, emoji="⛪")
    async def button_callback2(self, button, interaction):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)
        new_char = bloobot_classes.Character()
        new_char.current_hp = 15
        new_char.max_hp = 15
        new_char.int = 15
        new_char.str = 5
        new_char.dex = 5
        new_char.money = 90
        new_char.attack_skill = "Holy Blast"
        new_char.special_skill = "Heal"
        new_char.f_class = "Priest"
        characters[self.ctx.author.id] = new_char
        embed = discord.Embed(
        description="So You Are a Kind Priest I see,\nWe could use your holy magic to heal allies and smite down foes.",
        color=discord.Colour.blurple()
        )
        resume[self.ctx.author.id] = "ChooseArea"
        await self.ctx.respond("",embed=embed)

    @discord.ui.button(label="Mage", style=discord.ButtonStyle.blurple, emoji="🪄")
    async def button_callback3(self, button, interaction):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)
        new_char = bloobot_classes.Character()
        new_char.current_hp = 10
        new_char.max_hp = 10
        new_char.int = 30
        new_char.str = 5
        new_char.dex = 5
        new_char.money = 100
        new_char.attack_skill = "Fireball"
        new_char.special_skill = "Summon Ice Elemental"
        new_char.f_class = "Mage"
        characters[self.ctx.author.id] = new_char
        embed = discord.Embed(
        description="So You Are a Wise Mage I see,\nYour powerful magic abilities will prove to be beneficial",
        color=discord.Colour.blurple()
        )
        resume[self.ctx.author.id] = "ChooseArea"
        await self.ctx.respond("",embed=embed)
    
    @discord.ui.button(label="Archer", style=discord.ButtonStyle.blurple, emoji="🏹")
    async def button_callback4(self, button, interaction):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)
        new_char = bloobot_classes.Character()
        new_char.current_hp = 15
        new_char.max_hp = 15
        new_char.int = 5
        new_char.str = 15
        new_char.dex = 15
        new_char.money = 100
        new_char.attack_skill = "Double Shot"
        new_char.special_skill = "Stealth"
        new_char.f_class = "Archer"
        characters[self.ctx.author.id] = new_char
        embed = discord.Embed(
        description="So You Are a Masterful Archer I see,\nIf your aim is true then nothing will escape your",
        color=discord.Colour.blurple()
        )
        resume[self.ctx.author.id] = "ChooseArea"
        await self.ctx.respond("",embed=embed)


    async def interaction_check(self, interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("You are not allowed to interact with this",ephemeral=1)
            return False
        else:
            return True

class View(discord.ui.View):
    def __init__(self, ctx):
        self.ctx = ctx
        super().__init__()

    @discord.ui.button(label="Open the door", style=discord.ButtonStyle.blurple, emoji="🚪")
    async def button_callback1(self, button, interaction):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)
        embed = discord.Embed(
        description="You open the door.\nA old and scruffy man greets you.",
        color=discord.Colour.blurple()
        )
        resume[self.ctx.author.id] = "Pick"
        await self.ctx.respond("",embed=embed)

    @discord.ui.button(label="Ask who is it", style=discord.ButtonStyle.blurple, emoji="🤔")
    async def button_callback2(self, button, interaction):
        button.disabled = True
        button.label = "An Adventurer's Guild???"
        await interaction.response.edit_message(view=self)
        embed = discord.Embed(
        description="A voice shouts: \"We are from the Adventurer's Guild. Open the door if you are interested in joining\"",
        color=discord.Colour.blurple()
        )
        await self.ctx.respond("",embed=embed)

    @discord.ui.button(label="Go back to bed", style=discord.ButtonStyle.blurple, emoji="🛌")
    async def button_callback3(self, button, interaction):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)
        embed = discord.Embed(
        description="You hear the footsteps leaving your doorstep.\nYour adventure ended before it even began",
        color=discord.Colour.blurple()
        )
        await self.ctx.respond("",embed=embed)

    async def interaction_check(self, interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("You are not allowed to interact with this",ephemeral=1)
            return False
        else:
            return True

@bloobot.slash_command(name = "begin", description = "Journey Begins")
async def begin(ctx):
    embed = discord.Embed(
        title="Beginning",
        description="Placeholder (Do /adventure to continue)",
        color=discord.Colour.blurple()
    )
    resume[ctx.author.id] = "View"
    await ctx.respond("", embed=embed)

bloobot.run(os.getenv('TOKEN'))