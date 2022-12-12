import math
#class of given cone
class Cone():
    #a,b is horizonal coordinate, c is vertical height of tip
    #(x-self.a)**2 + (y-self.b)**2 = self.d**2 *(z-self.c)**2
    def __init__(self, a,b,c):
        self.a = a #x coordinate
        self.b = b #y coordinate
        self.c = 3*c/16 #altitude of cone
        self.angle = 56.457 * math.pi / 180 #angle of cone in radians
        #calculate radius of cone at ground level
        self.d = math.tan(self.angle) #1.508
        self.radius = self.d * self.c

    #return height of cone at x,y
    def height(self, x,y):
        return -math.sqrt((x-self.a)**2 + (y-self.b)**2)/self.d + self.c

    #return true if x,y on this cone is higher than cone2, which means cone2 is encompassed by cone
    def in_cone(self, cone2):
        if self.height(cone2.a,cone2.b) > cone2.c:
            #print(self.a,self.b,self.height(cone2.a,cone2.b),cone2.a,cone2.b,cone2.c)
            return True
        else:
            return False

        return self.height(cone2.a,cone2.b) >= cone2.c


#class of walker
class Walker():
    #walker starts on integer coordinates of circle of radius 28 center origin
    def __init__(self):
        self.alpha = 33.543 * math.pi / 180 #angle between cone and horizontal in radians
        self.theta = -47.854128647 * math.pi / 180 #theta value to maximise speed
        #speed can be 3 values, 2 for flat ground, 3.18413198711 for downhill, 0.796032996761 for uphill
        self.speed = [2, 3.18413198711, 0.796032996761] #self.speed[0] is flat ground, self.speed[1] is downhill, self.speed[-1] is uphill
        self.cones = find_cones()


    def time_over_distance(self,distance, gradient):
        return distance / self.speed[gradient]
    
    #returns distance between tip of cone1 and tip of cone2
    def distance_between_cones(self, cone1, cone2):
        return math.sqrt((cone1.a - cone2.a)**2 + (cone1.b - cone2.b)**2)

    #returns time taken to go from tip of cone1 down until either ground level or slope of cone2 is reached, then up slope of cone2 to tip of cone2
    def time_between_cones(self, cone1, cone2):
        distance = self.distance_between_cones(cone1, cone2)
        if distance >= cone1.radius + cone2.radius:
            return self.time_over_distance(cone1.radius,1) + self.time_over_distance(distance - cone1.radius - cone2.radius , 0) + self.time_over_distance(cone2.radius, -1)
        #if distance is less than sum of radii, then cone1 and cone2 overlap, so we need to find point of intersection of cones along the straight line between the 2 cones
        elif distance < cone1.radius + cone2.radius:
            if cone2.c < cone1.c:
                gradient = 1/math.tan(cone1.angle)
                cone2_to_intersection = distance*(cone1.c - cone2.c)/gradient
                cone1_to_intersection = distance - cone2_to_intersection
                return self.time_over_distance(cone1_to_intersection, 1) + self.time_over_distance(cone2_to_intersection, -1)
            elif cone2.c > cone1.c:
                gradient = 1/math.tan(cone2.angle)
                cone1_to_intersection = distance*(cone2.c - cone1.c)/gradient
                cone2_to_intersection = distance - cone1_to_intersection
                return self.time_over_distance(cone1_to_intersection, -1) + self.time_over_distance(cone2_to_intersection, 1)
            elif cone2.c == cone1.c:
                return self.time_over_distance(distance/2 , 1) + self.time_over_distance(distance/2 , -1)






#find all positive integer solutions to a**2 + b**2 + c**2 = 734
def find_solutions():
    solutions = []
    for a in range(1,28):
        for b in range(1,28):
            for c in range(1,28):
                if a**2 + b**2 + c**2 == 734:
                    solutions.append([a,b,c])
    return solutions


#make a cone at each solution
def find_cones():
    solutions = find_solutions()
    cones = []
    for solution in solutions:
        cones.append(Cone(solution[0],solution[1],solution[2]))


    #creates dictionary of cones with key = cone number and value = list of cones that are not encompassed by cone, or encompassing cone
    return_cones = {}
    for cone in cones:
        return_cones[cone] = []
        for cone2 in cones:
            if cone != cone2:
                if not cone.in_cone(cone2) and not cone2.in_cone(cone):
                    return_cones[cone].append(cone2)
                

    for cone in cones:
        if len(return_cones[cone]) <59:
            pass
            #print(cone.a,cone.b,cone.c,len(return_cones[cone]))
    

    return cones, return_cones          



List_of_cones,Array_of_cones = find_cones()
print(List_of_cones[56].a,List_of_cones[56].b,List_of_cones[56].c)
print(List_of_cones[59].a,List_of_cones[59].b,List_of_cones[59].c)
print(len(Array_of_cones[List_of_cones[56]]))

Sabrina = Walker()

#create dictionary in form {cone1: {cone2: time, cone3: time, ...}, cone4: {cone5: time, cone6: time, ...}, ...}
#where time is time taken to go from tip of cone1 down until either ground level or slope of cone2 is reached, then up slope of cone2 to tip of cone2
#and cone1 and cone2 are in the same list of cones
def create_dictionary_of_cones():
    dictionary_of_cones = {}
    for cone in List_of_cones:
        dictionary_of_cones[cone] = {}
        for cone2 in Array_of_cones[cone]:
            dictionary_of_cones[cone][cone2] = Sabrina.time_between_cones(cone,cone2)
    return dictionary_of_cones

dict_of_cones = create_dictionary_of_cones()

print(dict_of_cones[List_of_cones[59]][List_of_cones[55]])



#plot points of cones in geogebra to find cones in other cones
